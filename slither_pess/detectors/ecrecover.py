import re
from typing import List, Tuple

from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import (
    SolidityCall,
    Condition,
)
from slither.core.declarations import (
    FunctionContract,
)
from slither.core.cfg.node import Node
from slither.slithir.operations import LowLevelCall
from slither.analyses.data_dependency.data_dependency import is_dependent


class Ecrecover(AbstractDetector):
    """
    Detects not checked results of ecrecover
    """

    ARGUMENT = "pess-ecrecover"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "signer = ecrecover(hash, v, r, s)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/ecrecover.md"
    WIKI_TITLE = "Ecrecover"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = "Attacker can validate signatures from 0x0 address"
    WIKI_RECOMMENDATION = "Check the result of ecrecover"

    def analyze_function(
        self, function: FunctionContract
    ) -> List[Tuple[FunctionContract, Node, LowLevelCall, bool, bool]]:
        unchecked_results = set()
        var_to_node = {}
        for node in function.nodes:
            for ir in node.irs:
                try:
                    node_contains_0 = re.search(
                        r"address\((0|0x0*)\)", str(node)
                    )  # check if the node contains address(0|0x0..)
                    if isinstance(ir, SolidityCall):
                        if (
                            ir.function.name
                            == "ecrecover(bytes32,uint8,bytes32,bytes32)"
                        ):
                            unchecked_results.add(ir.lvalue)
                            var_to_node[ir.lvalue] = node
                        elif (
                            ir.function.name == "require(bool,string)"
                            or ir.function.name == "assert(bool)"
                        ):
                            if not node_contains_0:  # does not contain 0 check
                                continue
                            checking_var = ir.arguments[0]
                            for ur in unchecked_results:
                                if is_dependent(checking_var, ur, node):
                                    unchecked_results.remove(ur)
                                    break
                    elif isinstance(ir, Condition):
                        # this is copypaste, for now, couldn't figure out how to make this better without overcomplicating
                        if not node_contains_0:  # does not contain 0 check
                            continue
                        for ur in unchecked_results:
                            if is_dependent(ir.value, ur, node):
                                unchecked_results.remove(ur)
                                break

                except Exception as e:
                    print("failed", e)

        return [var_to_node[ur] for ur in unchecked_results]

    def _detect(self):
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                res = self.analyze_function(f)
                if res:
                    for r in res:
                        info = ["Unchecked result of ecrecover for 0:\n\t", r, "\n"]
                        tres = self.generate_result(info)
                        tres.add(r)
                        results.append(tres)
        return results
