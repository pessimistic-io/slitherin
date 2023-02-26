from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class StrangeSetter(AbstractDetector):
    """
    Sees if contract contains a setter, that does not change contract storage variables.
    """

    ARGUMENT = 'pess-strange-setter' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract storage parameter is not changed by setter'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://workflowy.com/#/692cf11bd6f1'
    WIKI_TITLE = 'Strange Setter'
    WIKI_DESCRIPTION = "Сеттеры должны менять значения storage переменных"
    WIKI_EXPLOIT_SCENARIO = 'Неработающий контракт'
    WIKI_RECOMMENDATION = 'Fix setter function'


    def _is_strange_setter(self, fun: Function) -> bool: 
        """Checks if setter sets smth to a storage variable and if function parameters are used when setting"""
        for fin in fun.internal_calls:  # branch with for-loop for setters in internal calls
            if isinstance(fin, Function):   # check for a correct function type
                for param in fin.parameters:
                    for n in fin.nodes:
                            if n.state_variables_written and str(param) in str(n):  # check if there's a state variable setter using function parameters
                                    return False
        if isinstance(fun, Function):   # check for a correct function type
            for param in fun.parameters: 
                for n in fun.nodes:
                    if n.state_variables_written and str(param) in str(n):  # check if there's a state variable setter using function parameters
                            return False
        return True


    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if not contract.is_interface:
                overriden_funtions = [] # functions that are overridden
                for f in contract.functions:
                    overriden_funtions.append(contract.get_functions_overridden_by(f))  # adding functions to an overridden list 
                    if f.name.startswith("set") and not f in overriden_funtions and len(f.nodes) != 0:  # check if setter starts with 'set', is not overriden and is not empty 
                        x = self._is_strange_setter(f)
                        if x:
                            res.append(self.generate_result([
                                "Function", ' ',
                                f, ' is a strange setter. ',
                                'Nothing is set or set without using function parameters'
                                '\n']))
        return res
