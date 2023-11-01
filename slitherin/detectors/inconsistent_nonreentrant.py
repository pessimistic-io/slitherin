from typing import List
from slither.utils.output import Output
from slither.core.declarations import Function
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


class InconsistentNonreentrant(AbstractDetector):
    """
    Sees if contract non-view functions do not have "nonreentrant" modifier while other functions have it.
    """

    ARGUMENT = 'pess-inconsistent-nonreentrant' # slither will launch the detector with slither.py --detect inconsistent-nonreentrant
    HELP = 'function ... (), function ... () nonReentrant'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/inconsistent_nonreentrant.md'
    WIKI_TITLE = 'Inconsistent nonreentrant'
    WIKI_DESCRIPTION = "If non-reentrant modifier is used then for security reasons it should be used in all non-veiw functions"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Make sure that all non-view functions use non-reentrant modifier'


    def _has_visibility_or_view(self, fun: Function) -> bool:
        """Function which checks if function is view or private/internal"""
        if fun.view:
            return True
        if fun.visibility in {'private', 'internal'}:
            return True

    def _has_modifiers(self, fun: Function) -> bool:
        """Function which checks modifiers on functions"""
        for m in fun.modifiers:
            if str(m.name) in 'nonReentrant':
                return True

    def _not_empty_function(self, fun: Function) -> bool:
        """Function which checks if given function is not empty"""
        if len(fun.nodes) != 0:
            return True

    def _validate_detection(self, contract_functions, nonreentrant_count) -> bool:
        """Function which validates the detection by comparing the number of functions and functions with nonReentrant"""
        contract_functions_length = len(contract_functions)
        nonreentrant_count_length = len(nonreentrant_count)
        if contract_functions_length == nonreentrant_count_length or nonreentrant_count_length == 0:
            return True

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        contract_functions = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                if f.name != "constructor" and not self._has_visibility_or_view(f) and self._not_empty_function(f):    # contstructor function is not checked
                    contract_functions.append(f)
                    if not self._has_modifiers(f):
                        res.append(self.generate_result([
                            "Function", ' ',
                            f, ' is a non-view function without nonReentrant modifier'
                            '\n']))
            invalid_detection = self._validate_detection(contract_functions, res)
            if invalid_detection:
                res.clear()
            return res
