from slither.core.cfg.node import NodeType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Contract, Function, SolidityVariableComposed
from slither.analyses.data_dependency.data_dependency import is_dependent


class DubiousTypecast(AbstractDetector):
    """
    Shows constant variables which are typecasted more than once.
    """

    ARGUMENT = 'dubious-typecast' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'uint8 = uint8(uint256)'
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = '-'
    WIKI_TITLE = 'Dubious Typecast'
    WIKI_DESCRIPTION = "Constant variables should not be typecasted more than once"
    WIKI_EXPLOIT_SCENARIO = 'Makes contract logic more complex'
    WIKI_RECOMMENDATION = 'Use clear constant variables'

    TYPECASTS = ["int","uint","bytes"]
    def hasDT(self, fun, params=None):
        # constVar = []
        for n in fun.nodes: # в первом приближении нода это строчка
            # if(fun.name == "slitherConstructorConstantVariables"):
            #     constVar.append(n.state_variables_written)
            for i in self.TYPECASTS:    
                for num in range(8, 128):
                    if(str(n).__contains__(f'{i}{num}(')):
                        return "True"

        return "False"

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self.hasDT(f)
                if (x != "False"):
                    res.append(self.generate_result([
                        'Function ',
                        f, ' has a dubious typecast '
                        '\n']))


        return res
