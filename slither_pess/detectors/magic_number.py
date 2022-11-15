import re
from slither.core.cfg.node import NodeType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


exceptions = ["0","1","2","1000","1e18"]


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
    WIKI_DESCRIPTION = "не должно быть числовых литералов без присваивания в константные переменные"
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'присваивать значения в константные переменные'

    
    def getLiterals(self, fun, params=None):
        res = []
        if(fun.name != "slitherConstructorConstantVariables"):
            for n in fun.nodes:
                nodeString = str(n)
                m = re.search(r'\s\d+e\d+|\s\d+', nodeString)
                if m:
                    digits = m[0].strip()
                    if digits not in exceptions:
                        res.append(digits)

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
