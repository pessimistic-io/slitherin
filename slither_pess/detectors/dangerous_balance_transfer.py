from pyclbr import Function
from typing import List
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


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

    def is_dangerous_balance_transfer(self, fun) -> str:
        _signatures = ["transfer(address,uint256)","transferFrom(address,address,uint256)","safeTransfer(IERC20,address,uint256)","safeTransferFrom(IERC20,address,address,uint256)"]
        for n in fun.nodes:
            for ir in n.irs:
                if ir.function.solidity_signature in _signatures:
                        if not self.has_access_control(fun) and str(n).__contains__("balanceOf" or "this"):
                            return "True"
                        if not self.has_access_control(fun) and self.amount_is_not_limited(fun):
                            return "True"
        return "False"

    def has_access_control(self, fun: Function) -> bool:
        for m in fun.modifiers:
            for m.name in ['initializer', 'onlyOwner']:
                return True

    def amount_is_not_limited(self, fun: Function) -> bool:
        for function_parameter in fun.parameters:
            if str(function_parameter.type) == "uint256":
                num_changes = 0
                for n in fun.nodes:
                    print(n)
                    print(function_parameter)
                    if str(n).__contains__(str(function_parameter)):
                        num_changes = num_changes+1
                    if num_changes >= 2:
                        return False
        print(fun)
        return True

    def _detect(self) -> List:

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self.is_dangerous_balance_transfer(f)
                if (x == "True"):
                    res.append(self.generate_result([
                        f, ' can transfer contract balance'
                        '\n']))


        return res