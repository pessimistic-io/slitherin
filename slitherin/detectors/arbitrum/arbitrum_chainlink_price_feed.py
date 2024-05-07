import os
import re
from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.analyses.data_dependency.data_dependency import is_dependent


from ...consts import ARBITRUM_KEY


class ArbitrumChainlinkPriceFeed(AbstractDetector):
    """
    Checks if sequencer uptime is verified when chainlink price feed is used
    """

    ARGUMENT = "pess-arb-chainlink-price-feed"  # slither will launch the detector with slither.py --detect mydetector

    HELP = "Sequencer uptime is not checked"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/arb_chainlink_price_feed.md"
    WIKI_TITLE = "Arbitrum chainlink sequencer uptime"
    WIKI_DESCRIPTION = "Arbitrum chainlink sequencer uptime check"
    WIKI_EXPLOIT_SCENARIO = "N/A"
    WIKI_RECOMMENDATION = "Check sequencer uptime (see docs)"

    def _contains_latest_round_call(self, f: Function) -> bool:
        ret = set()
        for node in f.nodes:
            for _, v in node.high_level_calls:
                if isinstance(v, Function) and v.name == "latestRoundData":
                    return True
        return False

    def _contains_sequencer_check(self, f: Function) -> bool:
        # Checks if the keyword sequencer used in function.
        # This check might contain FPs. However, since most of devs will copy-paste or get inspiration
        # from the chainlink docs, as for now, I think it should work well.

        for node in f.nodes:
            if re.search(r"sequencer", str(node), re.IGNORECASE):
                return True

        return False

    def _detect(self) -> List[Output]:
        """Main function"""
        results = []

        if os.getenv(ARBITRUM_KEY) is None:
            return results

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions_and_modifiers:
                if self._contains_latest_round_call(
                    f
                ) and not self._contains_sequencer_check(f):
                    info = [
                        "Sequencer uptime status is not checked when using price feed in:\n\t",
                        f,
                        "\nCheck https://docs.chain.link/data-feeds/l2-sequencer-feeds for more details\n",
                    ]
                    results.append(self.generate_result(info))
        return results
