import re
from collections import defaultdict
from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class MagicNumber(AbstractDetector):
    """
    Shows int/uint values which are not assigned to variables.
    """

    ARGUMENT = "pess-magic-number"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "int/uint values except 0, 1, 2, 1000 and 1e18"
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = (
        "https://github.com/pessimistic-io/slitherin/blob/master/docs/magic_number.md"
    )
    WIKI_TITLE = "Magic Number"
    WIKI_DESCRIPTION = "Values should be assigned to variables"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Assign values to variables"

    EXCEPTION = {"0", "1", "2", "1000", "1e18"}
    used_count = defaultdict(lambda: {"count": 0, "nodes": []})

    def _check_if_pow_10(self, str: str) -> bool:
        reg = re.fullmatch(r"^10*$|^10*e\d+$", str)  # 1(0..) or 1(0..)eX
        if reg:
            return True
        return False

    def _getLiterals(self, fun: Function) -> None:
        """Get numbers except those which are in EXCEPTION{}"""

        if (
            fun.name != "slitherConstructorConstantVariables"
        ):  # removing values assigned to constant variables
            for n in fun.nodes:
                nodeString = str(n)
                lit = re.search(
                    r"\W\d+e\d+|\W\d+[_*\d]*", nodeString
                )  # regular expression to get numbers
                if lit:
                    magic_number = lit[0]
                    index = (
                        len(magic_number) - 1
                    )  # get length of the found number and remove the space in the beginning
                    if magic_number[
                        -index:
                    ] not in self.EXCEPTION and not self._check_if_pow_10(
                        magic_number[-index:]
                    ):
                        result_number = magic_number[-index:]
                        self.used_count[result_number]["count"] += 1
                        self.used_count[result_number]["nodes"].append(n)

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        all_used_counts = []
        for contract in self.compilation_unit.contracts_derived:
            self.used_count = defaultdict(lambda: {"count": 0, "nodes": []})
            for f in contract.functions:
                self._getLiterals(f)
            all_used_counts.append(self.used_count)

        for contract_used_count in all_used_counts:
            for num, data in contract_used_count.items():
                if num:
                    if data["count"] < 2:
                        continue
                    info = [f"Magic number {num} is used multiple times in:\n"]
                    for n in data["nodes"]:
                        info += ["\t", n, "\n"]
                    res.append(self.generate_result(info))
        return res
