from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class TokenFallback(AbstractDetector):
    """
    Sees if a token contract has a fallback function.
    """

    ARGUMENT = 'pess-token-fallback' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'The contract has a fallback function'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/token_fallback.md'
    WIKI_TITLE = 'Token Fallback'
    WIKI_DESCRIPTION = "Fallback function in tokens must be used carefully"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Make sure that contract can not be exploited with fallback function'


    def _has_fallback(self, fun: Function) -> bool: 
        """Checks if token contract has a fallback function"""
        if fun.name == "fallback":
            return True
        return False

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_token:
                for function in contract.functions:
                    x = self._has_fallback(function)
                    if x:
                        res.append(self.generate_result([
                            "Token contract has a ",
                            function, ' which might be dangerous to implement',
                            '\n']))
        return res
