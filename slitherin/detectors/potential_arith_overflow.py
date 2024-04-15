from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.core.solidity_types.elementary_type import Int, Uint
from  slither.core.variables.local_variable import LocalVariable
import slither.slithir.operations as ops
import slither.slithir.variables as vrs
from slither.core.cfg.node import NodeType
import typing as tp

INT_TYPES = [*Int, *Uint]

class PotentialArithmOverflow(AbstractDetector):
    """
    Detects expressions where overflow may occur, but no overflow is expected
    """

    ARGUMENT = "pess-potential-arithmetic-overflow"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "Add explicit type casting in temporary expressions during the evaluation of arithmetic expressions in case the final type is larger than the intermediate one."
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = (
        "https://github.com/pessimistic-io/slitherin/blob/master/docs/potential_arith_overflow.md"
    )
    WIKI_TITLE = "Potential Arithmetic Overflow"
    WIKI_DESCRIPTION = "The detector sees if there are assignments/returns that calculate some arithmetic expressions and if some intermediate calculations contain a type that is lower than the expected result. Such behavior may lead to unexpected overflow/underflow, e.g., trying to assign the multiplication of two `uint48` variables to `uint256` would look like `uint48 * uint48` and it may overflow (however, the final type would fit such multiplication)."
    WIKI_EXPLOIT_SCENARIO = "A transaction will revert with overflow, but the expected behavior that it should not."
    WIKI_RECOMMENDATION = "Use explicit type casting in sub expressions when the assigment to a larger type is performed."
    
    def _has_op_overflowing_sub_expression(self, op: ops.Operation, high_level_bits_needed: tp.Optional[int]) -> (bool, list, str):
        if isinstance(op, ops.Unary):
            (is_err, nodes, sub_expr) = self._has_op_overflowing_sub_expression(op.rvalue, high_level_bits_needed) # ! and ~ do not affect result
            return (is_err, nodes, f"{op.type_str} {sub_expr}")
        elif isinstance(op, ops.Binary):
            result_type = str(op.lvalue.type)
            [l_check_res, l_check_list, l_sub_expr] = self._has_op_overflowing_sub_expression(op.variable_left, high_level_bits_needed)
            [r_check_res, r_check_list, r_sub_expr] = self._has_op_overflowing_sub_expression(op.variable_right, high_level_bits_needed)
                
            cur_expr = f"{l_sub_expr} {op._type.value} {r_sub_expr}"
            if op._type is ops.BinaryType.ADDITION or op._type is ops.BinaryType.MULTIPLICATION or op._type is ops.BinaryType.POWER:
                result_bits_cut = result_type.removeprefix("uint").removeprefix("int")
                result_bits = int(256 if not result_bits_cut else result_bits_cut)
                if high_level_bits_needed and high_level_bits_needed > result_bits: # result expects bigger type, but expression returns lower and overflow may occur here
                    return (True, [(cur_expr, result_type), *l_check_list, *r_check_list], cur_expr)
                else:
                    return (l_check_res or r_check_res, [*l_check_list, *r_check_list], cur_expr)
            else: # @todo currently we do not check other operations, return as everything is ok
                return (l_check_res or r_check_res, [*l_check_list, *r_check_list], cur_expr)
        elif isinstance(op, ops.OperationWithLValue):
            return (False, [], f"{op.lvalue}")
        elif isinstance(op, vrs.Constant):
            return (False, [], f"{op}")
        elif isinstance(op, LocalVariable):
            return (False, [], f"{op}")
        elif isinstance(op, vrs.state_variable.StateVariable):
            return (False, [], f"{op}")
        elif isinstance(op, vrs.TemporaryVariable):
            return (False, [], f"...")
        elif isinstance(op, ops.Return):
            return (False, [], f"{op}")
        elif isinstance(op, vrs.ReferenceVariable):
            return (False, [], f"{op}")
        else:
            return (False, [], f"{op}")

    def _find_vulnerable_expressions(self, fun: Function) -> list:
        final_results = []
        is_active_assembly = False
        for node in fun.nodes:
            if node.type is NodeType.ASSEMBLY:
                is_active_assembly = True
            elif node.type is NodeType.ENDASSEMBLY:
                is_active_assembly = False
            if (node.type is NodeType.VARIABLE or node.type is NodeType.EXPRESSION or node.type is NodeType.RETURN) and not is_active_assembly:
                irs = node.irs
                if len(irs) > 0 and isinstance(irs[-1], ops.Assignment) and str(irs[-1].lvalue._type) in INT_TYPES:
                    expected_bits_cut = str(irs[-1].lvalue._type).removeprefix("uint").removeprefix("int")
                    expected_bits = int(256 if not expected_bits_cut else expected_bits_cut)
                    has_problems = False
                    errors = []
                    for x in irs[:-1]:
                        (response_res, response_errors, _) = self._has_op_overflowing_sub_expression(x, expected_bits)
                        has_problems |= response_res
                        errors.extend(response_errors)
                    if has_problems:
                        final_results.append((node, str(irs[-1].lvalue._type), errors))
                if len(irs) > 0 and isinstance(irs[-1], ops.Return) and fun.return_type is not None and len(fun.return_type) == 1 and str(fun.return_type[0]) in INT_TYPES: # @todo currently works only with single returns
                    expected_bits_cut = str(fun.return_type[0]).removeprefix("uint").removeprefix("int")
                    expected_bits = int(256 if not expected_bits_cut else expected_bits_cut)
                    has_problems = False
                    errors = []
                    for x in irs[:-1]:
                        (response_res, response_errors, _) = self._has_op_overflowing_sub_expression(x, expected_bits)
                        has_problems |= response_res
                        errors.extend(response_errors)
                    if has_problems:
                        final_results.append((node, str(fun.return_type[0]), errors))

        return final_results
    
    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_interface:
                continue
            for f in contract.functions_and_modifiers_declared:
                vulnerable_expressions = self._find_vulnerable_expressions(f)
                if vulnerable_expressions:
                    info = [f, f" contains integer variables whose type is larger than the type of one of its intermediate expressions. Consider casting sub expressions explicitly as they might lead to unexpected overflow:\n"]
                    for (node, node_final_type, op_with_ret_type) in vulnerable_expressions:
                        info += ["\tIn `", node, "` intermidiate expressions returns type of lower order:", "\n"]
                        for (op, op_ret_type) in op_with_ret_type:
                            info += ["\t\t`", str(op), f"` returns {op_ret_type}, but the type of the resulting expression is {node_final_type}.", "\n"]
                    res.append(self.generate_result(info))
        return res