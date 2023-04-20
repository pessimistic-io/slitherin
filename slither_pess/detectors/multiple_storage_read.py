from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class MultipleStorageRead(AbstractDetector):
    """
    Sees if contract function reads the same storage variable multiple times.
    """

    ARGUMENT = 'pess-multiple-storage-read' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'The same contract storage variable is read multiple times in a function'
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/multiple_storage_read.md'
    WIKI_TITLE = 'Multiple Storage Read'
    WIKI_DESCRIPTION = "The same storage variable must not be read multiple times in the same function"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Consider creating and reading a local variable instead of a storage one if you read it more than once'


    def _has_multiple_storage_read(self, fun: Function) -> bool: 
        """Checks if function has multiple storage read"""
        if isinstance(fun, Function):   # check for a correct function type
            multiple_reads = []
            state_variables_used = []
            for n in fun.nodes: # check reads of state variables in nodes
                for node_state_variable in n.state_variables_read:
                    state_variables_used.append(node_state_variable)
            for function_state_variable in fun.state_variables_read: # check the number of times state variable are read
                indices = [i for i, x in enumerate(state_variables_used) if x == function_state_variable]
                if len(indices) > 2:
                    multiple_reads.append(function_state_variable)
            if multiple_reads:  
                return multiple_reads


    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions_and_modifiers_declared:
                x = self._has_multiple_storage_read(f)
                if x:
                    for multiple_read_var in x:
                        res.append(self.generate_result([
                            "In a function", ' ',
                            f, ' variable ', multiple_read_var , ' is read multiple times'
                            '\n']))
        return res
