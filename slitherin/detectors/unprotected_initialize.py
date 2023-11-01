from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function
from slither.core.variables.variable import Variable


class UnprotectedInitialize(AbstractDetector):
    """
    Sees if a contract has initialize functions that are not protected by anything.
    """

    ARGUMENT = "pess-unprotected-initialize"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "The contract must have its initialize function protected"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_initialize.md"
    WIKI_TITLE = "Unprotected Initialize"
    WIKI_DESCRIPTION = "Initializers must be protected"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Protect initializers with modifiers/require statements"

    def _is_initialize(self, fun: Function) -> bool:
        """Checks if function is initialize one"""
        if isinstance(fun, Function) and "init" in fun.name:
            return True
        return False

    def _has_modifiers(self, fun: Function) -> bool:
        """Checks if function has modifier protection"""
        for modifier in fun.modifiers:
            if str(modifier) == "onlyOwner" or str(modifier) == "initializer":
                return True
        return False

    def _has_require(self, fun: Function) -> bool:
        """Checks if function has require statement protection"""
        for node in fun.nodes:
            if "require" in str(node):
                for variable in node.variables_read:
                    if isinstance(variable, Variable):
                        if str(variable.type) == "address":
                            return True
        return False

    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_interface:
                continue
            for f in contract.functions_and_modifiers_declared:
                x = self._is_initialize(f)
                if x:
                    is_safe = self._has_modifiers(f)
                    is_safe2 = self._has_require(f)
                    if not is_safe and not is_safe2:
                        res.append(
                            self.generate_result(
                                [
                                    "Function ",
                                    f,
                                    " is an unprotected initializer.",
                                    "\n",
                                ]
                            )
                        )
        return res
