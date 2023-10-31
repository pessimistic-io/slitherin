import re
from typing import List, Tuple

from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import SolidityCall, Condition
from slither.core.declarations import (
    FunctionContract,
    SolidityVariableComposed,
    Function,
)
from slither.core.cfg.node import Node
from slither.slithir.operations import LowLevelCall
from slither.analyses.data_dependency.data_dependency import is_dependent


class AAVEFlashloanCallbackDetector(AbstractDetector):
    """
    Detects not checked results of ecrecover
    """

    ARGUMENT = "pess-aave-flashloan-callback"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "signer = ecrecover(hash, v, r, s)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/ecrecover.md"
    WIKI_TITLE = "Ecrecover"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = "Attacker can validate signatures from 0x0 address"
    WIKI_RECOMMENDATION = "Check the result of ecrecover"

    def _analyze_function(
        self,
        function: FunctionContract,
        args_to_verify,
        check_recursive=False,
        visited=[],
    ) -> Tuple[set, set]:
        checked = set()
        unchecked = set(args_to_verify)

        for node in function.nodes:
            if node.is_conditional(include_loop=False):  # contains if/assert/require
                for a in unchecked:
                    if any([is_dependent(arg, a, node) for arg in node.variables_read]):
                        checked.add(a)

        unchecked.difference_update(checked)  # remove all checked

        visited.append(function)
        if check_recursive:
            for node in function.nodes:
                for internal_call in node.internal_calls:
                    # Filter to Function, as internal_call can be a solidity call
                    if isinstance(internal_call, Function):
                        _checked, _unchecked = self._analyze_function(
                            internal_call, unchecked, False, visited
                        )  # We are going only 1 step into in recursion
                        checked |= _checked
                        unchecked = _unchecked

        return checked, unchecked

    def _detect(self):
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                if (
                    f.signature_str
                    == "executeOperation(address[],uint256[],uint256[],address,bytes) returns(bool)"
                ):
                    _, unchecked = self._analyze_function(
                        f,
                        [
                            SolidityVariableComposed("msg.sender"),
                            f.parameters[3],  # initiator parameter
                        ],
                        check_recursive=True,
                    )
                    if unchecked:
                        info = [
                            "Unchecked function parameters in AAVE callback: ",
                            f,
                            "\n",
                        ]
                        for var in unchecked:
                            if var == SolidityVariableComposed("msg.sender"):
                                info += ["\t", "'msg.sender' is not checked", "\n"]
                            else:
                                info += ["\t'", var.name, "' is not checked\n"]

                        tres = self.generate_result(info)
                        # for var in unchecked:
                        #     tres.add(var)
                        # tres.add(f)
                        results.append(tres)
        return results
