from slither.core.declarations import Function
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from typing import List


class DangerousBalanceTransfer(AbstractDetector):
    """
    Sees if contract contains a transfer of a contract balance
    """

    ARGUMENT = 'dangerous-balance-transfer' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract has a transfer of its balance'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://workflowy.com/#/6310b3446674'
    WIKI_TITLE = 'Dangerous Balance Transfer'
    WIKI_DESCRIPTION = "Contract balance can become 0"
    WIKI_EXPLOIT_SCENARIO = 'Contract transfers all its balance to a malicious address'
    WIKI_RECOMMENDATION = 'Be careful with contract balance transfers'

    def _is_dangerous_balance_transfer(self, fun: Function) -> bool:
        signatures = {"transfer(address,uint256)","transferFrom(address,address,uint256)","safeTransfer(IERC20,address,uint256)","safeTransferFrom(IERC20,address,address,uint256)"}
        for n in fun.nodes:
            for ir in n.irs:
                if ir.function.solidity_signature in signatures:
                        if not self._has_access_control(fun) and "balanceOf" in str(n) or "this" in str(n):
                            print(fun)
                            return True
                        if not self._has_access_control(fun) and self._amount_is_not_limited(fun):
                            return True
        return False

    def _has_access_control(self, fun: Function) -> bool:
        for m in fun.modifiers:
            if m.name is 'initializer' or 'onlyOwner':
                return True

    def _amount_is_not_limited(self, fun: Function) -> bool:
        for function_parameter in fun.parameters:
            if str(function_parameter.type) == "uint256":
                num_changes = 0
                for n in fun.nodes:
                    if str(function_parameter) in str(n):
                        num_changes = num_changes + 1
                    if num_changes >= 2:
                        return False
        return True

    def _detect(self) -> List:
        res = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self._is_dangerous_balance_transfer(f)
                if x is True:
                    res.append(self.generate_result([
                        f, ' can transfer contract balance'
                        '\n']))
        return res
