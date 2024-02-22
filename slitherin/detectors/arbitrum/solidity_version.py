import os
from typing import List
from slither.utils.output import Output
from slither.core.cfg.node import Node
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    make_solc_versions,
)
from slither.core.declarations import Function
from slither.slithir.operations.event_call import EventCall
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.slithir.operations import SolidityCall
from slither.core.declarations.solidity_variables import (
    SolidityVariableComposed,
    SolidityFunction,
)

from ...consts import ARBITRUM_KEY


class ArbitrumSolidityVersion(AbstractDetector):
    """
    Checks that sol version >= 0.8.20 is not used inside an Arbitrum contract
    """

    ARGUMENT = "pess-arb-solidity-version"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "sol version >= 0.8.20 is used in contract that will be deployed to Arbitrum (Potential usage of PUSH0, which is not supported)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/arb_difficulty_randao.md"
    WIKI_TITLE = "Arbitrum solidity version"
    WIKI_DESCRIPTION = "Potential usage of PUSH0 opcode"
    WIKI_EXPLOIT_SCENARIO = "N/A"
    WIKI_RECOMMENDATION = (
        "Either, use versions 0.8.19 and below, or EVM versions below shanghai"
    )

    def _detect(self) -> List[Output]:
        """Main function"""
        results = []

        if os.getenv(ARBITRUM_KEY) is None:
            return results

        if (
            self.compilation_unit.is_solidity
            and self.compilation_unit.solc_version in make_solc_versions(8, 20, 99)
        ):
            results.append(
                self.generate_result(
                    [
                        "Potential usage of solidity version >= 0.8.20 detected. Solidity in these versions will utilize PUSH0 opcode, ",
                        "which is not supported on Arbitrum. ",
                        "Either, use versions 0.8.19 and below, or EVM versions below shanghai",
                    ]
                )
            )

        return results
