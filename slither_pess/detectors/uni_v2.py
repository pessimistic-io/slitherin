import sys
import os
import json
from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function, Contract
from slither.slithir.operations.assignment import Assignment
from slither.core.expressions.type_conversion import TypeConversion


class UniswapV2(AbstractDetector):
    """
    Checks code for UniswapV2 integration vulnerabilities
    """

    ARGUMENT = 'pess-uni-v2' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Detector is based on UniswapV2 checklist'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://github.com/pessimistic-io/custom_detectors/blob/master/docs/integration_uniswapV2.md'
    WIKI_TITLE = 'UniswapV2 Integration'
    WIKI_DESCRIPTION = "UniswapV2 integration vulnerabilities must not be present in the codebase"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Follow UniswapV2 integration checklist'

    
    def _pair_balance_used(self, fun: Function) -> bool:
        """Checks if a function a uses pair balance"""
        mb_pair_vars = []
        for node in fun.nodes:
            if node.state_variables_read or node.local_variables_read:  # Checks if IUniswapV2Pair type is in local/storage vars
                for node_var in node.state_variables_read:
                    if str(node_var.type) == "IUniswapV2Pair":
                        mb_pair_vars.append(str(node_var))
                for node_var in node.local_variables_read:
                    if str(node_var.type) == "IUniswapV2Pair":
                        mb_pair_vars.append(str(node_var))
            for external_call in node.external_calls_as_expressions:    # Checks external calls for expressions with balanceOf
                if "balanceOf" in str(external_call):
                    for call_arg in external_call.arguments:
                        if isinstance(call_arg, TypeConversion):
                            if (    # Checks if IUniswapV2Pair is used in balanceOf
                                str(call_arg.expression) in mb_pair_vars or 
                                "IUniswapV2Pair" in str(call_arg.expression)
                            ):
                                return True
        return False

    def _pair_reserve_used(self, fun: Function) -> bool:
        """Checks if a function uses getReserves function of the Pair contract"""
        for external_call in fun.external_calls_as_expressions:
            if (
                "getReserves" in str(external_call) and
                "tuple" in external_call.type_call and 
                "function () view external returns (uint112,uint112,uint32)" in external_call.called.type
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
                if "IUniswapV2Pair" in str(node):   # Looking for IUniswapV2Pair in functions
                    return True
        return False


    def _minReturn_zero(self, fun: Function) -> bool:
        """Checks if a minReturn parameter equals zero"""
        calls_with_0_pos_argument = {   # Functions where minReturn is an argument at position 0
            "swapExactETHForTokens",
            "swapExactETHForTokensSupportingFeeOnTransferTokens"
        }
        calls_with_1_pos_argument = {   # Functions where minReturn is an argument at position 1
            "swapExactTokensForTokens",
            "swapExactTokensForETH",
            "swapExactTokensForTokensSupportingFeeOnTransferTokens",
            "swapExactTokensForETHSupportingFeeOnTransferTokens"
        }
        amountOutMin = ''
        for external_call in fun.external_calls_as_expressions: # Looking for a variable in the needed external call at positions 0 and 1
            if [call for call in calls_with_0_pos_argument if(call in str(external_call))] and external_call.arguments:
                amountOutMin = external_call.arguments[0]
            if [call for call in calls_with_1_pos_argument if(call in str(external_call))] and len(external_call.arguments) > 1:
                amountOutMin = external_call.arguments[1]
        if str(amountOutMin) == "0":    # If argument is set directly to 0 return True
            return True
        elif amountOutMin:  # Looking for 0 assignments to a variable found above
            for node in fun.nodes:
                for ir in node.irs:
                    if isinstance(ir, Assignment):
                        if str(ir.lvalue) == str(amountOutMin) and str(ir.rvalue) == "0":
                            return True
        return False

    def _maxReturn_max(self, fun: Function) -> bool:
        """Checks if a maxReturn parameter equals max"""
        calls_with_1_pos_argument = {   # Functions where minReturn is an argument at position 1
            "swapTokensForExactTokens",
            "swapTokensForExactETH"
        }
        amountInMax = ''
        tmp = ''
        for external_call in fun.external_calls_as_expressions: # Looking for a variable in the needed external call at position 1
            if [call for call in calls_with_1_pos_argument if(call in str(external_call))] and len(external_call.arguments) > 1:
                amountInMax = external_call.arguments[1]
        if str(amountInMax) == "type()(uint256).max":    # If argument is set directly to 0 return True
            return True
        elif amountInMax:  # Looking for max assignments to a variable found above
            for node in fun.nodes:
                for ir in node.irs:
                    if isinstance(ir, Assignment):
                        if (
                            "TMP_" in str(ir.lvalue) and 
                            str(ir.rvalue) == "115792089237316195423570985008687907853269984665640564039457584007913129639935"
                        ):
                            tmp = str(ir.lvalue)
                        if str(amountInMax) == str(ir.lvalue) and tmp == str(ir.rvalue):
                            return True
        return False

    #TODO детектить сет адресов в важных функциях через параметры, детектить в сторадж переменных
    def _has_bad_token(self, fun: Function) -> bool:
        """Checks if deflationary or rebase tokens are used"""
        absolute_path = os.path.dirname(__file__)
        relative_path = "../../utils/deflat_tokens.json"
        full_path = os.path.join(absolute_path, relative_path)
        fileJson = open(full_path)
        data = json.load(fileJson)
        objects = data['objects']
        for section in objects: # Looks for token addresses from json in nodes
            address = section['address']
            for node in fun.nodes:
                if address in str(node):
                    return True
        fileJson.close()
        return False

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        if "pess-uni-v2" in sys.argv:   # launch only if detector in terminal is present
            for contract in self.compilation_unit.contracts_derived:
                pair_used = self._pair_used(contract)
                for f in contract.functions:
                    pair_balance_used = self._pair_balance_used(f)
                    pair_reserve_used = self._pair_reserve_used(f)
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
