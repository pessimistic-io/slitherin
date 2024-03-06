from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function, Contract
from slither.core.cfg.node import Node
import re


class CurveReadonlyReentrancy(AbstractDetector):
    """
    Sees if a contract has a beforeTokenTransfer function.
    """

    ARGUMENT = "pess-curve-readonly-reentrancy"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "Curve readonly-reentrancy"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/curve_readonly_reentrancy.md"
    WIKI_TITLE = "Curve Readonly Reentrancy"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Check docs"

    VULNERABLE_FUNCTION_CALLS = ["get_virtual_price", "lp_price"]
    visited = []
    contains_reentrancy_check = {}

    def is_curve_integration(self, c: Contract) -> bool:
        """
        Iterates over all external function calls, and checks the interface/contract name
        for a specific keywords to decide if the contract integrates with balancer

        @note as for now, we are skipping any name/interface checks
        """

        return True

    def _has_reentrancy_check(self, node: Node) -> bool:
        if node in self.visited:
            return self.contains_reentrancy_check[node]

        self.visited.append(node)
        self.contains_reentrancy_check[node] = False

        for _, n in node.high_level_calls:
            if isinstance(n, Function):
                if not n.name:
                    continue
                if n.name == "withdraw_admin_fee":
                    self.contains_reentrancy_check[node] = True
                    return True

        # TODO: currently using regex to find address().call(*.withdraw_admin_fees)
        # It would be better, if it is rewritten in a ast analysis form

        if re.search(r"withdraw_admin_fee", str(node)):
            return True

        has_check = False
        for internal_call in node.internal_calls:
            if isinstance(internal_call, Function):
                for f_node in internal_call.nodes:
                    has_check |= self._has_reentrancy_check(f_node)

        self.contains_reentrancy_check[node] = has_check
        return has_check

    def _check_function(self, function: Function) -> list:
        has_dangerous_call = False
        dangerous_call = None
        for n in function.nodes:
            for c, fc in n.high_level_calls:
                if isinstance(fc, Function):
                    if fc.name in self.VULNERABLE_FUNCTION_CALLS:
                        dangerous_call = n  # Saving only first dangerous call
                        has_dangerous_call = True
                        break

        if has_dangerous_call and not any(
            [self._has_reentrancy_check(node) for node in function.nodes]
        ):
            return [dangerous_call]
        return []

    def _detect(self) -> List[Output]:
        """Main function"""
        result = []
        for contract in self.compilation_unit.contracts_derived:
            if not self.is_curve_integration(contract):
                continue
            res = []
            for f in contract.functions_and_modifiers_declared:
                function_result = self._check_function(f)
                if function_result:
                    res.extend(function_result)
            if res:
                info = [
                    "Curve readonly-reentrancy vulnerability detected in ",
                    contract,
                    ":\n",
                ]
                for r in res:
                    info += [
                        "\tThe answer of ",
                        r,
                        " call could be manipulated through readonly-reentrancy\n",
                    ]
                res = self.generate_result(info)
                res.add(r)
                result.append(res)

        return result
