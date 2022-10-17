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


    EXCEPTION = ["0","1","2","1000","1e18"]

    
    def getLiterals(self, fun, params=None):
        res = []

        for n in fun.nodes: # в первом приближении нода это строчка
            nodeString = str(n)
            lit = re.search(r'\d+e\d+|\d+', nodeString)
            if lit and not lit[0] in self.EXCEPTION:
                res.append(lit[0])

        return res

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self.getLiterals(f)
                if x:
                    pre = "magic number"
                    s = "s" if len(x)>1 else ""

                    res.append(self.generate_result([
                            "Function", ' ',
                            f, ' contains ' + pre + s + ': ' + ", ".join(x),
                            '\n']))


        return res
