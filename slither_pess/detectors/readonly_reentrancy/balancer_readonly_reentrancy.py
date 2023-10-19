from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function, Contract
from slither.core.cfg.node import Node


class BalancerReadonlyReentrancy(AbstractDetector):
    """
    Sees if a contract has a beforeTokenTransfer function.
    """

    ARGUMENT = "pess-balancer-readonly-reentrancy"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "beforeTokenTransfer function does not follow OZ documentation"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = (
        "https://docs.openzeppelin.com/contracts/4.x/extending-contracts#rules_of_hooks"
    )
    WIKI_TITLE = "Before Token Transfer"
    WIKI_DESCRIPTION = "Follow OZ documentation using their contracts"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = (
        "Make sure that beforeTokenTransfer function is used in the correct way."
    )

    VULNERABLE_FUNCTION_CALLS = ["getRate", "getPoolTokens"]
    visited = []
    contains_reentrancy_check = {}

    def is_balancer_integration(self, c: Contract) -> bool:
        """
        Iterates over all external function calls, and checks the interface/contract name
        for a specific keywords to decide if the contract integrates with balancer
        """
        for (
            fcontract,
            _,
        ) in c.all_high_level_calls:
            contract_name = fcontract.name.lower()
            if any(map(lambda x: x in contract_name, ["balancer", "ivault", "pool"])):
                return True

    def _has_reentrancy_check(self, node: Node) -> bool:
        if node in self.visited:
            return self.contains_reentrancy_check[node]

        self.visited.append(node)
        self.contains_reentrancy_check[node] = False

        for c, n in node.high_level_calls:
            if isinstance(n, Function):
                if (
                    n.name == "ensureNotInVaultContext"
                    and c.name == "VaultReentrancyLib"
                ) or (
                    n.name == "manageUserBalance"
                ):  # TODO check if errors out
                    self.contains_reentrancy_check[node] = True
                    return True

        has_check = False
        for internal_call in node.internal_calls:
            if isinstance(internal_call, Function):
                has_check |= self._has_reentrancy_check(internal_call)
                # self.contains_reentrancy_check[internal_call] |= has_check

        self.contains_reentrancy_check[node] = has_check
        return has_check

    def _check_function(self, function: Function) -> list:
        has_dangerous_call = False
        dangerous_call = None
        for n in function.nodes:
            for c, fc in n.high_level_calls:
                if isinstance(fc, Function):
                    if fc.name in self.VULNERABLE_FUNCTION_CALLS:
                        dangerous_call = fc
                        has_dangerous_call = True
                        break

        if has_dangerous_call and not any(
            [self._has_reentrancy_check(node) for node in function.nodes]
        ):
            print("READONLY_REENTRANCY!!!")

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if not self.is_balancer_integration(contract):
                continue
            for f in contract.functions_and_modifiers_declared:
                self._check_function(f)
        return res
