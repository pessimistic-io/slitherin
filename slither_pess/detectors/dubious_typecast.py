from slither.core.cfg.node import NodeType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Contract, Function, SolidityVariableComposed
from slither.analyses.data_dependency.data_dependency import is_dependent

from slither.slithir.operations import TypeConversion

def _getType(ir): # returns the last word of ir: "... type conversion to TYPENAME"
    return str(ir).split(" ")[-1]

def get_first_double_typecast_index(irs): # returns number

    for i in range(1,len(irs)):
        a=irs[i-1]
        b=irs[i]
        check = isinstance(a,TypeConversion) and isinstance(b, TypeConversion)
        # print(check)
        if check:
            return i-1

    return -1


class DubiousTypecast(AbstractDetector):
    """
    Shows constant variables which are typecasted more than once.
    """

    ARGUMENT = 'pess-dubious-typecast' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'uint8 = uint8(uint256)'
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/custom_detectors/blob/master/docs/dubious_typecast.md'
    WIKI_TITLE = 'Dubious Typecast'
    WIKI_DESCRIPTION = "Constant variables should not be typecasted more than once"
    WIKI_EXPLOIT_SCENARIO = 'Makes contract logic more complex, wich leads to error probability increment and make integration more difficult'
    WIKI_RECOMMENDATION = 'Use clear constants'

    def getDT(self, fun, params=None):

        res = []

        for n in fun.nodes: # в первом приближении нода это строчка

            r = get_first_double_typecast_index(n.irs)

            if r>-1:
                res.append(_getType(n.irs[r+1])+'<='+_getType(n.irs[r]))

        return res

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self.getDT(f)
                if x:
                    for j in x:
                        res.append(self.generate_result([
                            'Function ',
                            f, ' has a dubious typecast: ', j,
                            '\n']))


        return res
