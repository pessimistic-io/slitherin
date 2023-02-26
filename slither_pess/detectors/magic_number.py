import re
from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class MagicNumber(AbstractDetector):
    """
    Shows int/uint values which are not assigned to variables
    """

    ARGUMENT = 'pess-magic-number' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'int/uint values except 0, 1, 2, 1000 and 1e18'
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = '-'
    WIKI_TITLE = 'Magic Number'
    WIKI_DESCRIPTION = "не должно быть числовых литералов без присваивания в константные переменные"
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'присваивать значения в константные переменные'


    EXCEPTION = {"0","1","2","1000","1e18"}

    
    def _getLiterals(self, fun: Function) -> List[str]:
        """Get numbers except those which are in EXCEPTION{}"""
        res = []
        if(fun.name != "slitherConstructorConstantVariables"):  # removing values assigned to constant variables
            for n in fun.nodes:
                nodeString = str(n)
                lit = re.search(r'\W\d+e\d+|\W\d+', nodeString) # regular expression to get numbers
                if lit:
                    magic_number = lit[0]
                    index = len(magic_number) - 1   # get length of the found number and remove the space in the beginning
                    if not magic_number[-index:] in self.EXCEPTION:
                        result_number = magic_number[-index:]
                        res.append(result_number)

        return res

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self._getLiterals(f)
                if x:
                    pre = "magic number"
                    s = "s" if len(x) > 1 else ""
                    res.append(self.generate_result([
                            "Function", ' ',
                            f, ' contains ' + pre + s + ': ' + ", ".join(x),
                            '\n']))
        return res
