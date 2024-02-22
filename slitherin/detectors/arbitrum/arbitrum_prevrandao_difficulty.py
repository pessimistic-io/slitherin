import os
from typing import List
from slither.utils.output import Output
from slither.core.cfg.node import Node
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.slithir.operations.event_call import EventCall
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.slithir.operations import SolidityCall
from slither.core.declarations.solidity_variables import (
    SolidityVariableComposed,
    SolidityFunction,
)

from slitherin.consts import ARBITRUM_KEY


class ArbitrumPrevrandaoDifficulty(AbstractDetector):
    """
    Sees if `prevRandao` or `difficulty` is used inside an Arbitrum contract (as they return constant `1` in Arbitrum)
    """

    ARGUMENT = "pess-arb-prevrandao-difficulty"  # slither will launch the detector with slither.py --detect mydetector
    HELP = (
        "PrevRandao or difficulty is used in contract that will be deployed to Arbitrum"
    )
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/arb_difficulty_randao.md"
    WIKI_TITLE = "Usage of prevRandao/difficulty inside the Arbitrum contract"
    WIKI_DESCRIPTION = "Arbitrum prevRandao/difficulty"
    WIKI_EXPLOIT_SCENARIO = "N/A"
    WIKI_RECOMMENDATION = (
        "Do not use prevRandao/difficulty inside the code of an Arbitrum contract"
    )

    def _find_randao_or_difficulty(self, f: Function) -> List[Node]:
        ret = set()
        for node in f.nodes:
            for var in node.variables_read:
                if is_dependent(
                    var, SolidityVariableComposed("block.prevrandao"), node
                ) or is_dependent(
                    var, SolidityVariableComposed("block.difficulty"), node
                ):
                    ret.add(node)
            for ir in node.irs:
                if (
                    isinstance(ir, SolidityCall)
                    and ir.function == SolidityFunction("prevrandao()")
                    or isinstance(ir, SolidityCall)
                    and ir.function == SolidityFunction("difficulty()")
                ):
                    ret.add(node)
        return list(ret)

    def _detect(self) -> List[Output]:
        """Main function"""
        results = []

        if os.getenv(ARBITRUM_KEY) is None:
            return results

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions_and_modifiers:
                nodes = self._find_randao_or_difficulty(f)
                if nodes:
                    info = [
                        f,
                        " function uses prevRandao/difficulty inside the code of the Arbitrum contract\n",
                        "\tDangerous usages:\n",
                    ]

                    nodes.sort(key=lambda x: x.node_id)

                    for node in nodes:
                        info += ["\t- ", node, "\n"]

                    results.append(self.generate_result(info))
        return results
