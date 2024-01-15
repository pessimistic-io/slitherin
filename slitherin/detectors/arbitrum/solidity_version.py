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
    Sees if `block.number` or `block.timtestamp` is used inside an Arbitrum contract
    """

    ARGUMENT = "pess-arb-solidity-version"  # slither will launch the detector with slither.py --detect mydetector
    HELP = (
        "PrevRandao or difficulty is used in contract that will be deployed to Arbitrum"
    )
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/arb_difficulty_randao.md"
    WIKI_TITLE = "Usage of prevRandao/difficulty inside the Arbitrum contract"
    WIKI_DESCRIPTION = "Setter-functions must emit events"
    WIKI_EXPLOIT_SCENARIO = "N/A"
    WIKI_RECOMMENDATION = (
        "Do not use prevRandao/difficulty inside the code of an Arbitrum contract"
    )

    def _find_randao_or_difficulty(self, f: Function) -> List[Node]:
        ret = set()
        for node in f.nodes:
            for var in node.variables_read:
                if is_dependent(
                    var, SolidityVariableComposed("block.number"), node
                ) or is_dependent(
                    var, SolidityVariableComposed("block.timtestamp"), node
                ):
                    ret.add(node)
            for ir in node.irs:
                if (
                    isinstance(ir, SolidityCall)
                    and ir.function == SolidityFunction("number()")
                    or isinstance(ir, SolidityCall)
                    and ir.function == SolidityFunction("timestamp()")
                ):
                    ret.add(node)
        return list(ret)

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
                        "Usage of solidity version >= 0.8.20 detected. Solidity in these versions will utilize PUSH0 opcode, ",
                        "which is not supported on Arbitrum. ",
                        "Either, use versions 0.8.19 and below, or EVM versions below shanghai",
                    ]
                )
            )

        return results
