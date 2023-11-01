from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class StrangeSetter(AbstractDetector):
    """
    Sees if contract contains a setter, that does not change contract storage variables.
    """

    ARGUMENT = "pess-strange-setter"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "Contract storage parameter is not changed by setter"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = (
        "https://github.com/pessimistic-io/slitherin/blob/master/docs/strange_setter.md"
    )
    WIKI_TITLE = "Strange Setter"
    WIKI_DESCRIPTION = "Setter must write to storage variables"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Make sure that your setter actually sets something"

    def _is_strange_setter(self, fun: Function) -> bool:
        """Checks if setter sets smth to a storage variable and if function parameters are used when setting"""
        if not isinstance(fun, Function):
            return True

        if not fun.parameters:
            # nothing is in the params, so we don't care
            return False
        for (
            fin
        ) in fun.internal_calls:  # branch with for-loop for setters in internal calls
            if isinstance(fin, Function):
                for param in fin.parameters:
                    for n in fin.nodes:
                        if n.state_variables_written and str(param) in str(
                            n
                        ):  # check if there's a state variable setter using function parameters
                            return False
        for param in fun.parameters:
            if fun.state_variables_written:
                for n in fun.nodes:
                    if str(param) in str(n):
                        return False
        return True

    def _is_strange_constructor(self, fun: Function) -> bool:
        """Checks if constructor sets nothing"""
        return self._is_strange_setter(fun)

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if not contract.is_interface:
                overriden_funtions = []  # functions that are overridden
                for f in contract.functions:
                    if f.parameters:
                        x = False
                        overriden_funtions.append(
                            contract.get_functions_overridden_by(f)
                        )  # adding functions to an overridden list
                        if f.name == "constructor":
                            x = self._is_strange_constructor(f)
                        elif (
                            f.name.startswith("set")
                            and not f in overriden_funtions
                            and len(f.nodes) != 0
                        ):  # check if setter starts with 'set', is not overriden and is not empty
                            x = self._is_strange_setter(f)
                        if x:
                            res.append(
                                self.generate_result(
                                    [
                                        "Function",
                                        " ",
                                        f,
                                        " is a strange setter. ",
                                        "Nothing is set in constructor or set in a function without using function parameters"
                                        "\n",
                                    ]
                                )
                            )
        return res
