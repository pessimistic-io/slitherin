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


class ArbitrumBlockNumberTimestamp(AbstractDetector):
    """
    Sees if `block.number` or `block.timtestamp` is used inside an Arbitrum contract
    """

    ARGUMENT = "pess-arb-block-number-timestamp"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "`block.number` or `block.timtestamp` is used inside an Arbitrum contract"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/arb_block_number_timestamp.md"
    WIKI_TITLE = (
        "Usage of `block.number` or `block.timtestamp` inside the Arbitrum contract"
    )
    WIKI_DESCRIPTION = "# Arbitrum block.number/block.timestamp"
    WIKI_EXPLOIT_SCENARIO = "N/A"
    WIKI_RECOMMENDATION = "Look at docs for details"

    def _find_randao_or_difficulty(self, f: Function) -> List[Node]:
        ret = set()
        for node in f.nodes:
            for var in node.variables_read:
                if is_dependent(
                    var, SolidityVariableComposed("block.number"), node
                ) or is_dependent(
                    var, SolidityVariableComposed("block.timestamp"), node
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

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions_and_modifiers:
                nodes = self._find_randao_or_difficulty(f)
                if nodes:
                    info = [
                        f,
                        " function uses block.number/block.timestamp inside the code of the Arbitrum contract\n"
                        "They behave different than on Ethereum, for details: (https://docs.arbitrum.io/for-devs/concepts/differences-between-arbitrum-ethereum/block-numbers-and-time)\n",
                        "Verify, that contract's logic does not break because of these differences\n"
                        "\t Usages:\n",
                    ]

                    nodes.sort(key=lambda x: x.node_id)

                    for node in nodes:
                        info += ["\t- ", node, "\n"]

                    results.append(self.generate_result(info))
        return results
