import sys
from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class UniswapV2(AbstractDetector):
    """
    Checks code for UniswapV2 integration vulnerabilities
    """

    ARGUMENT = 'pess-uni-v2' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Detector is based on UniswapV2 checklist'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = '-'
    WIKI_TITLE = 'UniswapV2 Integration'
    WIKI_DESCRIPTION = "UniswapV2 vulnerabilities should not be present in the codebase"
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'Follow UniswapV2 integration checklist'

    
    def _pair_balance_used(self, fun: Function) -> List[str]:
        """Checks if a function a uses pair balance"""
        res = []
        return res

    def _pair_reserve_used(self, fun: Function) -> List[str]:
        """Checks if a function uses pair reserves"""
        res = []
        return res

    def _pair_used(self, fun: Function) -> List[str]:
        """Checks if a pair contract is used"""
        res = []
        return res

    def _minReturn_zero(self, fun: Function) -> List[str]:
        """Checks if a minReturn parameter equals zero"""
        res = []
        return res  

    def _maxReturn_max(self, fun: Function) -> List[str]:
        """Checks if a maxReturn parameter equals infinity"""
        res = []
        return res     

    def _has_bad_token(self, fun: Function) -> List[str]:
        """Checks if deflationary or rebase tokens are used"""
        res = []
        return res                 

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        if "pess-uni-v2" in sys.argv:
            for contract in self.compilation_unit.contracts_derived:
                pair_balance_used = self._pair_balance_used
                pair_reserve_used = self._pair_reserve_used
                pair_used = self._pair_used
                minReturn_zero = self._minReturn_zero
                maxReturn_max = self._maxReturn_max
                has_bad_token = self._has_bad_token
                for f in contract.functions:
                    if pair_balance_used:
                        res.append(self.generate_result(['Function ',f, ' uses pair balance.''\n']))
                    if pair_reserve_used:
                        res.append(self.generate_result({'Function ',f,' uses pair reserves.''\n' }))
                    if pair_used:
                        res.append(self.generate_result({'Contract ',contract,' uses pair contract directly.''\n' }))
                    if minReturn_zero:
                        res.append(self.generate_result({'Function ',f,' has a call of a swap with "min" parameter. Min parameter must not be 0''\n' }))
                    if maxReturn_max:
                        res.append(self.generate_result({'Function ',f,' has a call of a swap with "max" parameter. Max parameter must not be infinity''\n' }))
                    if has_bad_token:
                        res.append(self.generate_result({'Function ',f,' uses deflationary or rebase token''\n' }))                  
        return res
