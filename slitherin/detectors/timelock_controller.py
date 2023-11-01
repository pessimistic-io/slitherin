from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class TimelockController(AbstractDetector):
    """
    Sees if contract uses OZ TimelockController
    """

    ARGUMENT = 'pess-timelock-controller' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'The OZ implementation of timelock controller is used'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/timelock_controller.md'
    WIKI_TITLE = 'OZ Timelock Controller'
    WIKI_DESCRIPTION = "Delpoyer can bypass timelock limitations"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Revoke Proposer and Executor roles from the deployer of OZ Timelock Controller'


    def _function_timelock_controller (self, fun: Function) -> bool: 
        """Checks if function has multiple storage read"""
        if isinstance(fun, Function):   # check for a correct function type
            for parameter in fun.parameters:
                if str(parameter.type) == "TimelockController":
                    return True
            for n in fun.nodes: # check every node for a TimelockController
                if "TimelockController" in str(n):
                    return True
        return False

    def _state_var_timelock_controller (self, contract) -> bool:
        """Checks if state var contatins TimelockController"""
        for state_var in contract.state_variables:
            if str(state_var.type) == "TimelockController":
                return True
        return False

    def _inheritance_timelock_controller (self, contract) -> bool:
        """Check if TimelockController contract is inherited"""
        for inherited_contract in contract.inheritance:
            if str(inherited_contract.name) == "TimelockController":
                return True
        return False

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            found_in_inheritance = self._inheritance_timelock_controller(contract)
            found_in_state_var = self._state_var_timelock_controller(contract)
            for f in contract.functions_and_modifiers_declared:
                found_in_function = self._function_timelock_controller(f)
                if found_in_state_var or found_in_function or found_in_inheritance:
                    res.append(self.generate_result([
                        "In a contract", ' ',
                        contract, ' timelock-controller is used. Revoke deployer roles.'
                        '\n']))
        return res
