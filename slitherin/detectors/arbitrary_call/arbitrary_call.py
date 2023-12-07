from enum import Enum
from typing import List, Tuple
from collections import namedtuple

from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    classification_txt,
)
from slither.slithir.operations import SolidityCall, HighLevelCall
from slither.core.declarations import (
    Contract,
    SolidityVariableComposed,
    FunctionContract,
)
from slither.core.cfg.node import Node
from slither.slithir.operations import LowLevelCall
from slither.analyses.data_dependency.data_dependency import is_dependent, is_tainted


# TODO/Possible improvements:
# look for transferFroms if there is any transferFrom and contract contains whole arbitrary call - it is screwed
# Filter out role protected

DetectorParams = namedtuple(
    "DetectorParams", ["argument_suffix", "impact", "confidence"]
)


class ArbitraryCallDetectors:
    ArbitraryCallWithApproveStored = DetectorParams(
        "-with-stored-erc20-approves",
        DetectorClassification.HIGH,
        DetectorClassification.HIGH,
    )
    ArbitraryCall = DetectorParams(
        "",
        DetectorClassification.HIGH,
        DetectorClassification.HIGH,
    )
    ArbitraryCallDestinationTainted = DetectorParams(
        "-destination-tainted",
        DetectorClassification.MEDIUM,
        DetectorClassification.MEDIUM,
    )
    ArbitraryCallCalldataTainted = DetectorParams(
        "-calldata-tainted",
        DetectorClassification.MEDIUM,
        DetectorClassification.MEDIUM,
    )


class ArbitraryCall(AbstractDetector):
    """
    Detects arbitrary and dangerous calls.
    (only detects low-level calls)
    """

    ARGUMENT = "pess-arbitrary-call"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "someaddress.call(somedata)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = (
        "https://github.com/pessimistic-io/slitherin/blob/master/docs/arbitrary_call.md"
    )
    WIKI_TITLE = "Arbitrary calls"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = "Attacker can manipulate on inputs"
    WIKI_RECOMMENDATION = "Do not allow arbitrary calls"

    def _is_role_protected(self, function: FunctionContract):
        for m in function.modifiers:
            if m.name.startswith("only"):
                return True
        return False

    def analyze_function(
        self, function: FunctionContract
    ) -> Tuple[
        List[Tuple[FunctionContract, Node, LowLevelCall, bool, bool]], bool
    ]:  # TODO(yhtiyar): make return type as named tuple/class
        results = []
        stores_approve = False
        for node in function.nodes:
            for ir in node.irs:
                try:
                    destination_tainted = False
                    args_tainted = False
                    if isinstance(ir, LowLevelCall):
                        destination_tainted = is_tainted(ir.destination, node, True)
                        if (
                            destination_tainted
                            and ir.destination == SolidityVariableComposed("msg.sender")
                        ):
                            # We don't care about msg.sender, since will be only reentrancy issue
                            destination_tainted = False
                        args_tainted = any(
                            is_tainted(arg, node, True) for arg in ir.arguments
                        )  # seems like ir.arguments = [data] for all low-level calls

                    elif (
                        isinstance(ir, SolidityCall)
                        and ir.function.name
                        == "delegatecall(uint256,uint256,uint256,uint256,uint256,uint256)"
                    ):
                        # delegatecall
                        destination_tainted = is_tainted(ir.arguments[1], node, True)
                        # #args_tainted = is_tainted(ir.arguments[2], node, True)
                        # for delegateCall we don't actually care about args, since
                        # for all proxies, user fully sets args
                    elif (
                        isinstance(ir, SolidityCall)
                        and ir.function.name
                        == "call(uint256,uint256,uint256,uint256,uint256,uint256,uint256)"
                    ):
                        # call()
                        destination_tainted = is_tainted(ir.arguments[1], node, True)
                        args_tainted = is_tainted(ir.arguments[3], node, True)

                    elif (
                        isinstance(ir, HighLevelCall)
                        and ir.function.name == "transferFrom"
                    ):
                        stores_approve = True

                    if args_tainted or destination_tainted:
                        results.append(
                            (
                                function,
                                node,
                                ir,
                                args_tainted,
                                destination_tainted,
                            )
                        )
                except Exception as e:
                    print("ArbitraryCall:Failed to check types", e)
                    print(ir)

        return (results, stores_approve)

    def analyze_contract(self, contract: Contract):
        stores_approve = False
        all_tainted_calls: List[
            Tuple[FunctionContract, Node, LowLevelCall, bool, bool]
        ] = []
        results = []
        for f in contract.functions:
            (res, _stores_approve) = self.analyze_function(f)
            stores_approve |= _stores_approve
            if res:
                all_tainted_calls.extend(res)

        for call_fn, node, ir, args_tainted, destination_tainted in all_tainted_calls:
            info = ["Manipulated call found: ", node, " in ", call_fn, "\n"]
            if args_tainted and destination_tainted:
                text = "Both destination and calldata could be manipulated"
            else:
                part = "calldata" if args_tainted else "destination"
                text = f"Only the {part} could be manipulated"
            info += [f"{text}\n"]

            for f in contract.functions:
                if f.visibility not in ["external", "public"]:
                    continue
                if self._is_role_protected(f):
                    continue

                fn_taints_args = False
                fn_taints_destination = False
                args = (
                    ir.arguments[0] if isinstance(ir, LowLevelCall) else ir.arguments[3]
                )
                if args_tainted and any(
                    is_dependent(args, fn_arg, node) for fn_arg in f.variables
                ):
                    fn_taints_args = True

                destination = (
                    ir.destination if isinstance(ir, LowLevelCall) else ir.arguments[1]
                )
                if destination_tainted and any(
                    is_dependent(destination, fn_arg, node) for fn_arg in f.variables
                ):
                    fn_taints_destination = True

                if not (fn_taints_args or fn_taints_destination):
                    continue

                detectorParams: DetectorParams = None
                if fn_taints_args and fn_taints_destination:
                    if stores_approve:
                        text = "The call could be fully manipulated (arbitrary call). This contract also STORES APPROVES!!!"
                        detectorParams = (
                            ArbitraryCallDetectors.ArbitraryCallWithApproveStored
                        )

                    else:
                        text = "The call could be fully manipulated (arbitrary call)"
                        detectorParams = ArbitraryCallDetectors.ArbitraryCall
                else:
                    if fn_taints_args:
                        part = "calldata"
                        detectorParams = (
                            ArbitraryCallDetectors.ArbitraryCallCalldataTainted
                        )

                    else:
                        part = "destination"
                        detectorParams = (
                            ArbitraryCallDetectors.ArbitraryCallDestinationTainted
                        )

                    text = f"The {part} could be manipulated"
                info += [f"\t{text} through ", f, "\n"]

                res = self.generate_result(info)
                res.add(node)
                res.data["check"] = self.ARGUMENT + detectorParams.argument_suffix
                res.data["impact"] = classification_txt[detectorParams.impact]
                res.data["confidence"] = classification_txt[detectorParams.confidence]

                results.append(res)
        return results

    def _detect(self):
        results = []
        for contract in self.compilation_unit.contracts_derived:
            r = self.analyze_contract(contract)
            if r:
                results.extend(r)
        return results
