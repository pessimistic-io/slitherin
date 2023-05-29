from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class UnprotectedInitialize(AbstractDetector):
    """
    Sees if a contract has initialize functions that are not protected by anything.
    """

    ARGUMENT = 'pess-unprotected-initialize' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'The contract must have its initialize function protected'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_initialize.md'
    WIKI_TITLE = 'Unprotected Initialize'
    WIKI_DESCRIPTION = "Initializers must be protected"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Protect initializers with modifiers/require statements'


    def _is_initialize(self, fun: Function) -> bool: 
        """Checks if function is initialize one"""
        if isinstance(fun, Function) and "init" in fun.name:
            return True
        return False
    
    def _has_access_control(self, fun):
        for m in fun.modifiers:
            for m.name in ['initializer', 'onlyOwner']:
                return True
        if fun.visibility in ['internal','private']:
            return True
        for node in fun.nodes:
            if "require" in str(node):
                for variable in node.variables_read:
                    if str(variable.type) == "address":
                        return True
        return fun.is_protected()
    
    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if not contract.is_library:
                for f in contract.functions:
                    if not self.has_access_control(f):
                        x = self.is_initialize(f)
                        if (x!= None):
                            res.append(self.generate_result([
                                "Function ",
                                f, ' is an unprotected initializer.',
                                '\n']))
        return res
