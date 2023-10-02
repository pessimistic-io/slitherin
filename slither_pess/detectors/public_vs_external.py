from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Contract


class PublicVsExternal(AbstractDetector):
    """
    Detects functions that have "public" modifiers and not used in the contract
    """

    ARGUMENT = "pess-public-vs-external"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "mark public functions as external where possible, to enhance contract's control-flow readability"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/public_vs_external.md"
    WIKI_TITLE = "Public vs External"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = "No exploits, just readability enhancement"
    WIKI_RECOMMENDATION = "Mark public functions as external where it is possible"

    def _analyze_contract(self, contract: Contract) -> list:
        res = []
        used_functions = set()
        for f in contract.functions_and_modifiers_declared:
            for node in f.nodes:
                for call in node.internal_calls:
                    used_functions.add(call.name)

        for f in contract.functions_and_modifiers_declared:
            if f.visibility == "public" and f.name not in used_functions:
                res.append(f)
        return res

    def _detect(self) -> List[Output]:
        """Main function"""
        results = []
        for contract in self.compilation_unit.contracts_derived:
            res = self._analyze_contract(contract)
            if res:
                info = [
                    "The following public functions could be turned into external in ",
                    contract,
                    " contract:\n",
                ]
                for r in res:
                    info += ["\t", r, "\n"]
                contract_result = self.generate_result(info)
                results.append(contract_result)

        return results
