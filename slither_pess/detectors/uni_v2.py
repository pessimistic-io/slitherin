import sys
from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.core.expressions.type_conversion import TypeConversion


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

    
    #TODO детектить предварительные присваивания. См. test - pair_token_balance_used_3
    def _pair_balance_used(self, fun: Function) -> bool:
        """Checks if a function a uses pair balance"""
        mb_pair_vars = []
        for node in fun.nodes:
            if node.state_variables_read or node.local_variables_read:  # Check if IUniswapV2Pair type is in local/storage vars
                for node_var in node.state_variables_read:
                    if str(node_var.type) == "IUniswapV2Pair":
                        mb_pair_vars.append(str(node_var))
                for node_var in node.local_variables_read:
                    if str(node_var.type) == "IUniswapV2Pair":
                        mb_pair_vars.append(str(node_var))
            for external_call in node.external_calls_as_expressions:    # Check external calls for expressions with balanceOf
                if "balanceOf" in str(external_call):
                    for call_arg in external_call.arguments:
                        if isinstance(call_arg, TypeConversion):
                            if str(call_arg.expression) in mb_pair_vars or "IUniswapV2Pair" in str(call_arg.expression):    # Check if IUniswapV2Pair is used in balanceOf
                                return True
        return False

    def _pair_reserve_used(self, fun: Function) -> List[str]:
        """Checks if a function uses getReserves function of the Pair contract"""
        for external_call in fun.external_calls_as_expressions:
            if (
                "getReserves" in str(external_call) and
                "tuple" in external_call.type_call and 
                "function () view external returns (uint112,uint112,uint32)" in external_call.called.type
            ): 
                return True
        return False

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
                for f in contract.functions:
                    pair_balance_used = self._pair_balance_used(f)
                    pair_reserve_used = self._pair_reserve_used(f)
                    pair_used = self._pair_used(f)
                    minReturn_zero = self._minReturn_zero(f)
                    maxReturn_max = self._maxReturn_max(f)
                    has_bad_token = self._has_bad_token(f)
                    if pair_balance_used:
                        res.append(self.generate_result(['Function ',f, ' uses pair balance.''\n']))
                    if pair_reserve_used:
                        res.append(self.generate_result(['Function ',f,' uses pair reserves.''\n']))
                    if pair_used:
                        res.append(self.generate_result(['Contract ',contract,' uses pair contract directly.''\n']))
                    if minReturn_zero:
                        res.append(self.generate_result(['Function ',f,' has a call of a swap with "min" parameter. Min parameter must not be 0''\n']))
                    if maxReturn_max:
                        res.append(self.generate_result(['Function ',f,' has a call of a swap with "max" parameter. Max parameter must not be infinity''\n']))
                    if has_bad_token:
                        res.append(self.generate_result(['Function ',f,' uses deflationary or rebase token''\n']))                  
        return res
