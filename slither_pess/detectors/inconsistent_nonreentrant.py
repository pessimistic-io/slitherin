from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

from typing import List
from slither.core.cfg.node import Node
from slither.core.declarations.solidity_variables import SolidityVariable
from slither.slithir.operations import LibraryCall
from slither.core.declarations import Contract, Function, SolidityVariableComposed
from slither.analyses.data_dependency.data_dependency import is_dependent


class InconsistentNonreentrant(AbstractDetector):
    """
    Sees if contract non-view functions do not have "nonreentrant" modifier while other functions have it
    """

    ARGUMENT = 'inconsistent-nonreentrant' # slither will launch the detector with slither.py --detect inconsistent-nonreentrant
    HELP = 'function ... (), function ... () nonreentrant'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://workflowy.com/s/40d940743275/G8dJAU9ahhPNuSCY#/b3637d2987cb'
    WIKI_TITLE = 'Inconsistent nonreentrant'
    WIKI_DESCRIPTION = "Если используется non-reentrant модификатор, то обычно он должен быть на всех non-veiw методах "
    WIKI_EXPLOIT_SCENARIO = 'Атакующий может сделать реентранси атаку, вызвав реентрант функцию через reentrancy-point в nonReentrant функции'
    WIKI_RECOMMENDATION = 'Убедиться, что все non-view функции используют non-reentrant'


