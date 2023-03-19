from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class BeforeTokenTransfer(AbstractDetector):
    """
    Sees if contract beforeTokenTransfer function is not right.
    """

    ARGUMENT = 'pess-before-token-transfer' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'beforeTokenTransfer function does not follow OZ documentation'
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://docs.openzeppelin.com/contracts/4.x/extending-contracts#rules_of_hooks'
    WIKI_TITLE = 'Before Token Transfer'
    WIKI_DESCRIPTION = "Follow OZ documentation using their contracts"
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'Make sure that beforeTokenTransfer function is used in the correct way.'


    def _has_no_virtual (self, fun: Function) -> bool: 
        """Checks if function does not have virtual modifier"""
        if isinstance(fun, Function):   # check for a correct function type
            print(fun.source_mapping) # reads function modifiers
        return False

    def _has_no_super (self, fun: Function) -> bool:
        """Checks if parent function call has super"""


    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            print(contract.modifiers)
            for f in contract.functions_and_modifiers_declared:
                x = self._has_no_virtual(f)
                y = self._has_no_super(f)
                z = True
                if x or y or z:
                    res.append(self.generate_result([
                        "beforeTokenTransfer in ",
                        f, ' does not have virtual or super.',
                        '\n']))
        return res
