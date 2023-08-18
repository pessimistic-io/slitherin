from typing import List, Optional, Tuple
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import TypeConversion, Operation
from slither.core.declarations import (
    Contract,
    SolidityVariableComposed,
    FunctionContract,
)
from slither.core.cfg.node import Node
from slither.slithir.operations import LowLevelCall
from slither.analyses.data_dependency.data_dependency import is_dependent, is_tainted


# TODO:
# look for transferFroms if there is any transferFrom and contract contains whole arbitrary call - it is screwed
# Construct callstack on how the destination/args could be tainted


class ArbitraryCall(AbstractDetector):
    """
    Detects arbitrary and dangerous calls.
    (only detects low-level calls)
    """

    ARGUMENT = "pess-arbitrary-call"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "someaddress.call(somedata)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/dubious_typecast.md"
    WIKI_TITLE = "Arbitrary calls"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = "Attacker can manipulate on inputs"
    WIKI_RECOMMENDATION = "Do not allow arbitrary calls"

    def analyze_function(self, function: FunctionContract) -> List[Tuple[str, str]]:
        results = []
        for node in function.nodes:
            for ir in node.irs:
                try:
                    if isinstance(ir, LowLevelCall):
                        destination_tainted = is_tainted(ir.destination, node, True)
                        if destination_tainted and ir.destination == "this":
                            # TODO: check this
                            destination_tainted = False
                        args_tainted = any(
                            is_tainted(arg, node, True) for arg in ir.arguments
                        )  # seems like ir.arguments = [data] for all low-level calls

                        if destination_tainted and args_tainted:
                            # attacker can manipulate on the whole call
                            results.append(f"The whole call is tainted:{node}")
                            print(f"The whole call is tainted:{node}")
                        elif destination_tainted:
                            results.append(f"The destination tainted:{node}")
                            print(f"The destination tainted:{node}")
                        elif args_tainted:
                            results.append(f"The whole call is tainted:{node}")
                            print(f"The whole call is tainted:{node}")

                except Exception as e:
                    print("ArbitraryCall:Failed to check types", e)
                    print(ir)

        return results

    def analyze_contract(self, contract: Contract):
        stores_approve = False
        for f in contract.functions:
            res = self.analyze_function(f)
            if res:
                print(contract, res)

    def _detect(self):
        results = []
        for contract in self.compilation_unit.contracts_derived:
            self.analyze_contract(contract)
            # for f in contract.functions:
            #     func_res = self.get_dubious_typecasts(f)
            #     if func_res:
            #         info = ["Dubious typecast in ", f, ":\n"]
            #         for node, node_res in func_res:
            #             for from_type, to_type in node_res:
            #                 info += [
            #                     f"\t{str(from_type)} => {str(to_type)} casting occurs in ",
            #                     node,
            #                     "\n",
            #                 ]
            #         res = self.generate_result(info)
            #         res.add(f)
            #         results.append(res)

        return results
