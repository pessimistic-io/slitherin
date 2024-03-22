from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.slithir.operations.event_call import EventCall


class EventSetter(AbstractDetector):
    """
    Sees if contract setters do not emit events
    """

    ARGUMENT = 'pess-event-setter' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract function does not emit event after the value is set'
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/event_setter.md'
    WIKI_TITLE = 'Missing Event Setter'
    WIKI_DESCRIPTION = "Setter-functions must emit events"
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'Emit events in setter functions'


    def _emits_event(self, fun: Function) -> bool: 
        """Checks if function has multiple storage read"""
        if isinstance(fun, Function):   # check for a correct function type
            if any(ir for node in fun.nodes for ir in node.irs if isinstance(ir, EventCall)):
                return True
            return False

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if not contract.is_interface:
                for f in contract.functions_and_modifiers_declared:
                    if f.name.startswith("set"):
                        x = self._emits_event(f)
                        if not x:
                            res.append(self.generate_result([
                                "Setter function ",
                                f, ' does not emit an event'
                                '\n']))
        return res
