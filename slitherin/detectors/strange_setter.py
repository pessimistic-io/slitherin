from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
import slither.core.expressions.new_array as na
import slither.core.expressions.new_contract as nc
from slither.analyses.data_dependency.data_dependency import is_dependent


class StrangeSetter(AbstractDetector):
    """
    Sees if contract contains a setter, that does not change contract storage variables or that does not use arguments for an external call.
    """

    ARGUMENT = "pess-strange-setter"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "Contract storage parameter is not changed by setter"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = (
        "https://github.com/pessimistic-io/slitherin/blob/master/docs/strange_setter.md"
    )
    WIKI_TITLE = "Strange Setter"
    WIKI_DESCRIPTION = "Setter must write to storage variables or pass arguments to external calls"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Make sure that your setter actually sets something"

    def _is_strange_setter(self, fun: Function) -> bool:
        """Checks if setter sets smth to a storage variable and if function parameters are used when setting"""
        if not isinstance(fun, Function):
            return True

        if not fun.parameters:
            # nothing is in the params, so we don't care
            return False
        used_params = set()
        for (
            fin
        ) in fun.internal_calls:  # branch with for-loop for setters in internal calls
            if isinstance(fin, Function):
                for param in fin.parameters:
                    for n in fin.nodes:
                        if n.state_variables_written and str(param) in str(
                            n
                        ):  # check if there's a state variable setter using function parameters
                            used_params.add(param)
        for param in fun.parameters:
            if fun.state_variables_written:
                for n in fun.nodes:
                    if str(param) in str(n):
                        used_params.add(param)
        for param in fun.parameters:
            for external in fun.external_calls_as_expressions:
                if isinstance(external._called, na.NewArray):
                    continue
                if isinstance(external._called, nc.NewContract): # skip new contract calls, idk how to get arguments passed to creation
                    continue
                for arg in [*external.arguments, external._called._expression]:
                    if str(arg) == str(param):
                        used_params.add(param)
        if fun.name == "constructor":
            for base_call in fun.explicit_base_constructor_calls:
                if not self._is_strange_constructor(base_call):
                    for param_cur in fun.parameters:
                        for param_base in base_call.parameters:
                            if is_dependent(param_base, param_cur, base_call):
                                used_params.add(param_cur)
        intersection_len = len(set(fun.parameters) & used_params)
        return intersection_len != len(fun.parameters)

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
