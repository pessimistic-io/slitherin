from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import LowLevelCall
from slither.core.declarations import Function
from slither.utils.output import Output
from typing import List


class CallForwardToProtected(AbstractDetector):
    """
    Shows cases when contract calls custom addresses and has contract interactions through access control
    """

    ARGUMENT = 'pess-call-forward-to-protected' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract might have a call to a custom address'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/call_forward_to_protected.md'
    WIKI_TITLE = 'Call Forward To Protected'
    WIKI_DESCRIPTION = "No calls to custom addresses and contract interactions through access control"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Do not let calls to project contracts or do not give rights to a contract which can perform calls'

    
    def _contains_low_level_calls(self, node) -> bool:
        return any(isinstance(ir, LowLevelCall) for ir in node.irs)

    def _detect_low_level_custom_address_call(self, fun: Function) -> bool:
        address_parameters = [
            parameter for parameter in fun.parameters if str(parameter.type) == "address" and parameter.name
        ]
        for node in fun.nodes:
            if self._contains_low_level_calls(node):
                for address_parameter in address_parameters:
                    if str(address_parameter) in str(node):
                        return True
        return False

    def _detect(self) -> List[Output]:
        res = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self._detect_low_level_custom_address_call(f)
                if x:
                    res.append(self.generate_result([
                            "Function", ' ',
                            f, ' contains a low level call to a custom address',
                            '\n']))

        return res
