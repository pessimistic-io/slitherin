from slither.core.cfg.node import NodeType

from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


class InconsistentNonreentrant(AbstractDetector):
    """
    Sees if contract non-view functions do not have "nonreentrant" modifier while other functions have it
    """

    ARGUMENT = 'inconsistent-nonreentrant' # slither will launch the detector with slither.py --detect inconsistent-nonreentrant
    HELP = 'function ... (), function ... () nonReentrant'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://workflowy.com/s/40d940743275/G8dJAU9ahhPNuSCY#/b3637d2987cb'
    WIKI_TITLE = 'Inconsistent nonreentrant'
    WIKI_DESCRIPTION = "Если используется non-reentrant модификатор, то обычно он должен быть на всех non-veiw методах "
    WIKI_EXPLOIT_SCENARIO = 'Атакующий может сделать реентранси атаку, вызвав реентрант функцию через reentrancy-point в nonReentrant функции'
    WIKI_RECOMMENDATION = 'Убедиться, что все non-view функции используют non-reentrant'


    def has_nonreentrant(self, fun):

        if fun.view:
            return True

        for m in fun.modifiers:
            for m.name in 'nonReentrant':
                return True

        return fun.is_protected()

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                if not self.has_nonreentrant(f):
                    res.append(self.generate_result([
                        f.contract_declarer.name, ' ',
                        f.name, ' is a non-view function without nonReentrant modifier'
                        '\n']))

        return res