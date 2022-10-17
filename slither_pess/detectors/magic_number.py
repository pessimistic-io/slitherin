import re
from slither.core.cfg.node import NodeType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


class MagicNumber(AbstractDetector):
    """
    Shows int/uint values which are not assigned to variables
    """

    ARGUMENT = 'magic-number' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'int/uint values except 0, 1, 2, 1000 and 1e18'
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = '-'
    WIKI_TITLE = 'Magic Number'
    WIKI_DESCRIPTION = "не должно быть числовых литералов без присваивания в переменные"
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'присваивать значения в константные переменные'


    
    def hasLiteral(self, fun, params=None):
        x = "False"
        for n in fun.nodes: # в первом приближении нода это строчка
            nodeString = str(n)
            lit = re.search(r'\d+', nodeString)
            if(lit != None):
                if(lit[0] != "0" and lit[0] != "1" and lit[0] != "2" and lit[0] != "1000" and lit[0] != "1e18"):
                    print(lit[0])
                    pattern = re.compile('([^!=] = \d+)|(([^!=]=\d+))|([^!=] = -\d+)|(([^!=]=-\d+))')
                    x = pattern.match(nodeString)
                    if(x != True):
                        return "True"
        return "False"

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self.hasLiteral(f)
                if (x != "False"):
                    res.append(self.generate_result([
                            "Function", ' ',
                            f, ' has a int/uint value which is not assigned to a variable'
                            '\n']))


        return res
