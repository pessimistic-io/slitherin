from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.slithir.operations.event_call import EventCall

VULNERABLE_VERSIONS = ['0.2.15', '0.2.16', '0.3.0']
class CurveVyperReentrancy(AbstractDetector):
    ARGUMENT = 'pess-curve-vyper-reentrancy' # slither will launch the detector with slither.py --detect mydetector
    HELP = f'Vyper compiler versions {", ".join(VULNERABLE_VERSIONS)} are vulnerable to malfunctioning re-entrancy guards. Upgrade your compiler version.'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/curve_vyper_reentrancy.md'
    WIKI_TITLE = 'Vulnerable Vyper version'
    WIKI_DESCRIPTION = "Some Vyper versions are vulnerable to malfunctioning re-entrancy guards."
    WIKI_EXPLOIT_SCENARIO = 'https://hackmd.io/@LlamaRisk/BJzSKHNjn'
    WIKI_RECOMMENDATION = 'Upgrade the version of your Vyper compiler.'

    def _detect(self) -> List[Output]:
        res = []
        if not self.compilation_unit.is_vyper:
            return res
        compiler_version = self.compilation_unit.compiler_version.version
        if compiler_version not in VULNERABLE_VERSIONS:
            return res
        
        for contract in self.contracts:
            for f in contract.functions_entry_points:
                for modifier in f.modifiers:
                    if modifier.name.startswith("nonreentrant"):
                        res += ["\t", modifier.name, " in ", f, " function.\n"]
        if not res:
            return res
        return [self.generate_result(
            [f"Vyper {compiler_version} compiler version is vulnerable to malfunctioning re-entrancy guards. Found vulnerable usages:\n",
             *[x for x in res],
             "\n"
            ]
        )]
