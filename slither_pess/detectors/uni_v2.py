from logging import Logger
import sys
import os
import json
import copy
from typing import List, Optional
from slither import Slither
from slither.core.compilation_unit import SlitherCompilationUnit
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function, Contract
from slither.core.expressions.type_conversion import TypeConversion
from slither.core.cfg.node import Node
from slither.core.variables.local_variable import LocalVariable
from slither.core.solidity_types.array_type import ArrayType
from slither.slithir.operations import InternalCall, HighLevelCall
from slither.slithir.operations.assignment import Assignment
from slither.analyses.data_dependency.data_dependency import is_dependent


class Context:
    def __init__(
        self,
        c: Contract,
        entry_point: Function,
        func: Function,
        args_tainted_mask: List[bool],
        verbose: bool,
    ):
        self.visited = []
        self.contract = c
        self.entry_point = entry_point
        self.hit_function = None
        self.tainted_path = []
        self.param_name = None
        self.function = func
        self.args_tainted_mask = args_tainted_mask  # TODO remove as this is redundant (covered by entrypoint_params_index_dependency)
        self.entrypoint_params_index_dependency: List[List[int]] = [
            [i] for i in range(len(entry_point.parameters))
        ]
        self.call_chain = [entry_point.name]
        self.hits = []
        self.verb = verbose

    def make_copy(self):  # to avoid passing by reference in internal calls inspections
        cp = copy.copy(self)
        cp.call_chain = copy.copy(self.call_chain)
        cp.entrypoint_params_index_dependency = copy.copy(
            self.entrypoint_params_index_dependency
        )
        return cp

    def __str__(self):  # debug
        return (
            "entry_point"
            + str(self.entry_point)
            + "hit_function"
            + str(self.hit_function)
            + "param_name"
            + str(self.param_name)
        )


class Hit:
    def __init__(
        self,
        entry_point: Function,
        hit_function: Function,
        param_name,
        call_chain: List[str],
        entry_params_used: List[str],
        swap_func: str,
    ):
        self.entry_point = entry_point
        self.hit_function = hit_function
        self.param_name = param_name
        self.call_chain = call_chain
        self.entry_params_used = entry_params_used
        self.swap_func = swap_func


swap_functions = [
    "swapExactTokensForTokens",
    "swapTokensForExactTokens",
    "swapExactTokensForTokensSupportingFeeOnTransferTokens",
    "swapExactETHForTokensSupportingFeeOnTransferTokens",
    "swapExactTokensForETHSupportingFeeOnTransferTokens",
    "swapETHForExactTokens",
    "swapExactTokensForETH",
    "swapTokensForExactETH",
    "swapExactETHForTokens",
    "getAmountsOut",
    "getAmountsIn",
]
swap_route_arg_pos = [2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1]

# widespread false positives
banned_funcs = ["ensure", "constructor"]
# partial (LIKE %x%)
banned_funcs_partial = []
banned_contracts_partial = ["swap", "dex", "router", "pancake", "buysell"]


def check_contract(c: Contract) -> List[Function]:
    results_raw: List[Function] = []

    if len(swap_functions) != len(swap_route_arg_pos):
        print("ERROR - Array lengths not matching")
        return results_raw
    # skip test contracts
    if any(x in c.name for x in ["Test", "Mock"]) or any(
        x in c.name.lower() for x in banned_contracts_partial
    ):
        return results_raw

    # to filter constructors for old solidity versions
    inherited_contracts = get_inherited_contracts(c) + [c.name]

    # filter unwanted funcs (also checked later recursively for nested calls)
    to_inspect = (
        x
        for x in c.functions
        if (
            # filter banned functions and old solc constructors
            x.name not in (banned_funcs + inherited_contracts)
            and not any(y in x.name for y in banned_funcs_partial)
            and not x.pure
            and not x.view
            and x.visibility in ["public", "external"]
            and x.is_implemented  # internal functions inspected through internal calls to keep the flow consistent
        )
    )

    for f in to_inspect:
        verb = False
        if f.name == "-":
            verb = True
        ctx = Context(c, f, f, [True for i in range(len(f.parameters))], verb)
        check_function(f.entry_point, ctx)
        if len(ctx.hits):
            results_raw += ctx.hits
    return results_raw


def check_function(node: Optional[Node], ctx: Context):
    if node is None:
        return False

    if ctx.function.name in banned_funcs or any(
        x in ctx.function.name for x in banned_funcs_partial
    ):
        return False

    if is_modifier_protected(ctx.function):  # TODO enhance
        return False

    if node in ctx.visited:
        return False
    ctx.visited.append(node)

    # debug
    if ctx.verb:
        print(str(node))
        for ir in node.irs:
            print("    " + str(ir) + "    " + str(type(ir)))

    # check if the input parameters are checked, and remove taint flag if so
    if (
        node.contains_if()
        or node.contains_require_or_assert()
        and "address(0)" not in str(node)
    ):
        for i in range(len(ctx.function.parameters)):
            param = ctx.function.parameters[i]
            if isinstance(param, LocalVariable) and not isinstance(
                param.type, ArrayType
            ):  # only look for checks on single addresses, not on path (which most likely will be length)
                if param in node.local_variables_read:
                    ctx.args_tainted_mask[i] = False
                    ctx.entrypoint_params_index_dependency[i] = False

    for ir in node.irs:
        # check for external calls
        if isinstance(ir, HighLevelCall):
            for i in range(len(swap_functions)):  # check if
                if (
                    hasattr(ir.function, "name")
                    and ir.function.name == swap_functions[i]
                    and len(ir.arguments) >= swap_route_arg_pos[i] + 1
                ):
                    path_argument = ir.arguments[swap_route_arg_pos[i]]
                    tainted_indexes = is_dependent_on_any_tainted(
                        path_argument,
                        ctx.function.parameters,
                        ctx.args_tainted_mask,
                        ctx.function,
                    )
                    if len(tainted_indexes):
                        if not (
                            ctx.function.name == ctx.entry_point.name
                            and ctx.function.name in swap_functions
                        ):
                            _ctx = ctx.make_copy()
                            # list entry parameters used to compute the route
                            entry_params_used = []
                            for (
                                ti
                            ) in (
                                tainted_indexes
                            ):  # indici dei parametri della funzione corrente, da cui dipende la path
                                for pi in ctx.entrypoint_params_index_dependency[
                                    ti
                                ]:  # indici dei parametri dell'entrypoint
                                    entry_params_used.append(
                                        ctx.entry_point.parameters[pi].name
                                    )
                            ctx.hits.append(
                                Hit(
                                    _ctx.entry_point,
                                    _ctx.function,
                                    path_argument.name,
                                    _ctx.call_chain,
                                    entry_params_used,
                                    swap_functions[i],
                                )
                            )

        # internal call to inspect
        elif isinstance(ir, InternalCall):
            # prepare new context for the callee
            ctx_callee = ctx.make_copy()
            ctx_callee.call_chain.append(ir.function.name)
            # map tainted bool mask from caller parameters to callee arguments
            taint_mask = []
            ctx_callee.entrypoint_params_index_dependency = [
                [] for i in range(len(ir.arguments))
            ]  # empty out to fill in the coming loop
            for i in range(len(ir.arguments)):
                carg = ir.arguments[i]
                tainted_indexes = is_dependent_on_any_tainted(
                    carg, ctx.function.parameters, ctx.args_tainted_mask, ctx.function
                )
                taint_mask.append(True if len(tainted_indexes) else False)
                for ti in tainted_indexes:
                    for epi in ctx.entrypoint_params_index_dependency[ti]:
                        ctx_callee.entrypoint_params_index_dependency[i].append(epi)

            ctx_callee.args_tainted_mask = taint_mask
            ctx_callee.function = ir.function
            check_function(ir.function.entry_point, ctx_callee)
            if len(ctx_callee.hits) > len(ctx.hits):  # callee has new hits
                for i in range(len(ctx_callee.hits), len(ctx.hits)):
                    ctx.hits.append(ctx_callee.hits[i])

    # sons inspection
    ret = False
    for son in node.sons:
        ret = ret or check_function(
            son, ctx
        )  # ctx by reference to get it populated with flags
    return ret


def is_dependent_on_any_tainted(
    checked_var: LocalVariable,
    vars_list: List[LocalVariable],
    tainted_mask: List[bool],
    context,
) -> List[int]:
    ret: List[int] = []
    if not type(checked_var) is list:  # can be list eg foo([bar, 0], par)
        checked_var = [checked_var]
    for i in range(len(checked_var)):
        if not isinstance(checked_var[i], LocalVariable):
            continue
        if not len(vars_list) == len(tainted_mask):
            print("ERROR: Mismatch array length vars_list vs tainted_mask")
            return []
        for j in range(len(vars_list)):
            if not tainted_mask[j]:
                continue
            if is_dependent(checked_var[i], vars_list[j], context):
                ret.append(j)
    return ret


def get_inherited_contracts(contract: Contract) -> List[str]:
    return list(x.name for x in contract.inheritance)


def is_modifier_protected(func: Function) -> bool:
    bannedPattern = [
        "admin",
        "owner",
        "role",
        "only",
        "permission",
        "initializ",
        "auth",
    ]
    for mod in func.modifiers:
        if any(x in mod.name.lower() for x in bannedPattern):
            return True
    return False


class UniswapV2(AbstractDetector):
    """
    Checks code for UniswapV2 integration vulnerabilities
    """

    ARGUMENT = "pess-uni-v2"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "Detector is based on UniswapV2 checklist"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/integration_uniswapV2.md"
    WIKI_TITLE = "UniswapV2 Integration"
    WIKI_DESCRIPTION = (
        "UniswapV2 integration vulnerabilities must not be present in the codebase"
    )
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Follow UniswapV2 integration checklist"

    def __init__(
        self, compilation_unit: SlitherCompilationUnit, slither: Slither, logger: Logger
    ) -> None:
        super().__init__(compilation_unit, slither, logger)
        absolute_path = os.path.dirname(__file__)
        relative_path = "../utils/deflat_tokens.json"
        full_path = os.path.join(absolute_path, relative_path)
        fileJson = open(full_path)
        data = json.load(fileJson)
        self.token_objects = data["objects"]
        fileJson.close()

    def _pair_balance_used(self, fun: Function) -> bool:
        """Checks if a function a uses pair balance"""
        mb_pair_vars = []
        for node in fun.nodes:
            if (
                node.state_variables_read or node.local_variables_read
            ):  # Checks if IUniswapV2Pair type is in local/storage vars
                for node_var in node.state_variables_read:
                    if str(node_var.type) == "IUniswapV2Pair":
                        mb_pair_vars.append(str(node_var))
                for node_var in node.local_variables_read:
                    if str(node_var.type) == "IUniswapV2Pair":
                        mb_pair_vars.append(str(node_var))
            for (
                external_call
            ) in (
                node.external_calls_as_expressions
            ):  # Checks external calls for expressions with balanceOf
                if "balanceOf" in str(external_call):
                    for call_arg in external_call.arguments:
                        if isinstance(call_arg, TypeConversion):
                            if str(  # Checks if IUniswapV2Pair is used in balanceOf
                                call_arg.expression
                            ) in mb_pair_vars or "IUniswapV2Pair" in str(
                                call_arg.expression
                            ):
                                return True
        return False

    def _pair_reserve_used(self, fun: Function) -> bool:
        """Checks if a function uses getReserves function of the Pair contract"""
        for external_call in fun.external_calls_as_expressions:
            if (
                "getReserves" in str(external_call)
                and "tuple" in external_call.type_call
                and "function () view external returns (uint112,uint112,uint32)"
                in external_call.called.type
            ):
                return True
        return False

    def _pair_used(self, contract: Contract) -> bool:
        """Checks if a Pair contract is used"""
        for var in contract.variables:  # Looking for a IUniswapV2Pair type var
            if str(var.type) == "IUniswapV2Pair":
                return True
        for function in contract.functions:
            for node in function.nodes:
                if "IUniswapV2Pair" in str(
                    node
                ):  # Looking for IUniswapV2Pair in functions
                    return True
        return False

    def _minReturn_zero(self, fun: Function) -> bool:
        """Checks if a minReturn parameter equals zero"""
        calls_with_0_pos_argument = (
            {  # Functions where minReturn is an argument at position 0
                "swapExactETHForTokens",
                "swapExactETHForTokensSupportingFeeOnTransferTokens",
            }
        )
        calls_with_1_pos_argument = (
            {  # Functions where minReturn is an argument at position 1
                "swapExactTokensForTokens",
                "swapExactTokensForETH",
                "swapExactTokensForTokensSupportingFeeOnTransferTokens",
                "swapExactTokensForETHSupportingFeeOnTransferTokens",
            }
        )
        amountOutMin = ""
        for (
            external_call
        ) in (
            fun.external_calls_as_expressions
        ):  # Looking for a variable in the needed external call at positions 0 and 1
            if [
                call
                for call in calls_with_0_pos_argument
                if (call in str(external_call))
            ] and external_call.arguments:
                amountOutMin = external_call.arguments[0]
            if [
                call
                for call in calls_with_1_pos_argument
                if (call in str(external_call))
            ] and len(external_call.arguments) > 1:
                amountOutMin = external_call.arguments[1]
        if str(amountOutMin) == "0":  # If argument is set directly to 0 return True
            return True
        elif amountOutMin:  # Looking for 0 assignments to a variable found above
            for node in fun.nodes:
                for ir in node.irs:
                    if isinstance(ir, Assignment):
                        if (
                            str(ir.lvalue) == str(amountOutMin)
                            and str(ir.rvalue) == "0"
                        ):
                            return True
        return False

    def _maxReturn_max(self, fun: Function) -> bool:
        """Checks if a maxReturn parameter equals max"""
        calls_with_1_pos_argument = (
            {  # Functions where minReturn is an argument at position 1
                "swapTokensForExactTokens",
                "swapTokensForExactETH",
            }
        )
        amountInMax = ""
        tmp = ""
        for (
            external_call
        ) in (
            fun.external_calls_as_expressions
        ):  # Looking for a variable in the needed external call at position 1
            if [
                call
                for call in calls_with_1_pos_argument
                if (call in str(external_call))
            ] and len(external_call.arguments) > 1:
                amountInMax = external_call.arguments[1]
        if (
            str(amountInMax) == "type()(uint256).max"
        ):  # If argument is set directly to 0 return True
            return True
        elif amountInMax:  # Looking for max assignments to a variable found above
            for node in fun.nodes:
                for ir in node.irs:
                    if isinstance(ir, Assignment):
                        if (
                            "TMP_" in str(ir.lvalue)
                            and str(ir.rvalue)
                            == "115792089237316195423570985008687907853269984665640564039457584007913129639935"
                        ):
                            tmp = str(ir.lvalue)
                        if str(amountInMax) == str(ir.lvalue) and tmp == str(ir.rvalue):
                            return True
        return False

    def _has_bad_token(self, fun: Function) -> bool:
        """Checks if deflationary or rebase tokens are used"""

        for (
            section
        ) in self.token_objects:  # Looks for token addresses from json in nodes
            address = section["address"]
            for node in fun.nodes:
                if address in str(node):
                    return True

        return False

    def _contract_uses_uniswap(self, c: Contract) -> bool:
        for (
            fcontract,
            _,
        ) in c.all_high_level_calls:
            if "uniswapv2" in fcontract.name.lower():
                return True

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        results_raw: List[Hit] = []
        results: List[Output] = []

        for contract in self.compilation_unit.contracts_derived:
            contains_uni_v2 = self._contract_uses_uniswap(contract)
            if (
                not contains_uni_v2 and not "pess-uni-v2" in sys.argv
            ):  # launch only if detector in terminal is present or there is dependency
                continue
            results_raw += check_contract(contract)

            for f in results_raw:
                info = [
                    f"Tainted route '",
                    f.param_name,
                    "' for function '",
                    f.swap_func,
                    "'\n in function '",
                    f.hit_function,
                    "'\n from entry point '",
                    f.entry_point,
                    "'\n Call chain (one of the possible ones): ",
                    str(f.call_chain),
                    "\n Entrypoint params used: ",
                    str(f.entry_params_used),
                    "\n\n",
                ]
                res.append(self.generate_result(info))
            pair_used = self._pair_used(contract)
            for f in contract.functions:
                pair_balance_used = self._pair_balance_used(f)
                pair_reserve_used = self._pair_reserve_used(f)
                minReturn_zero = self._minReturn_zero(f)
                maxReturn_max = self._maxReturn_max(f)
                has_bad_token = self._has_bad_token(f)
                if pair_balance_used:
                    res.append(
                        self.generate_result(
                            ["Function ", f, " uses pair balance." "\n"]
                        )
                    )
                if pair_reserve_used:
                    res.append(
                        self.generate_result(
                            ["Function ", f, " uses pair reserves." "\n"]
                        )
                    )
                if pair_used:
                    res.append(
                        self.generate_result(
                            [
                                "Contract ",
                                contract,
                                " uses pair contract directly." "\n",
                            ]
                        )
                    )
                if minReturn_zero:
                    res.append(
                        self.generate_result(
                            [
                                "Function ",
                                f,
                                ' has a call of a swap with "min" parameter. Min parameter must not be 0'
                                "\n",
                            ]
                        )
                    )
                if maxReturn_max:
                    res.append(
                        self.generate_result(
                            [
                                "Function ",
                                f,
                                ' has a call of a swap with "max" parameter. Max parameter must not be infinity'
                                "\n",
                            ]
                        )
                    )
                if has_bad_token:
                    res.append(
                        self.generate_result(
                            [
                                "Function ",
                                f,
                                " uses deflationary or rebase token" "\n",
                            ]
                        )
                    )
        return res
