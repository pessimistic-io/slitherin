from typing import List, Tuple
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import TypeConversion, Operation
from slither.core.declarations import FunctionContract
from slither.core.cfg.node import Node


def is_ok_cast(from_type: str, to_type: str) -> bool:
    if from_type == to_type:
        return True
    if from_type == "address" or to_type == "address":
        # address <-> interface/contract/this
        # address <-> uint160 (solidity doesn't allow other direct casts of address)
        return True

    if "bytes" in from_type and "bytes" in to_type:
        # bytesX <-> bytesY will have different results
        return False

    if "bytes" in from_type or "bytes" in to_type:
        return True

    if "uint" == from_type[:4] and "uint" in to_type[:4]:
        size_from = from_type[4:]
        if size_from == "":
            size_from = "256"

        size_to = to_type[4:]
        if to_type == "":
            size_to = "256"

        if int(size_from) > int(size_to):
            return False
        return True

    if "int" == from_type[:3] and "int" == to_type[:3]:
        size_from = from_type[3:]
        if size_from == "":
            size_from = "256"

        size_to = to_type[3:]
        if to_type == "":
            size_to = "256"

        if int(size_from) > int(size_to):
            return False
        return True

    sorted_types = sorted([from_type, to_type])
    if "int" == sorted_types[0][:3] and "uint" == sorted_types[1][:4]:
        return False

    return True


class DubiousTypecast(AbstractDetector):
    """
    Shows nonstandard typecasts.
    """

    ARGUMENT = "pess-dubious-typecast"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "uint8 = uint8(uint256)"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/dubious_typecast.md"
    WIKI_TITLE = "Dubious Typecast"
    WIKI_DESCRIPTION = "Check docs"
    WIKI_EXPLOIT_SCENARIO = (
        "Can produce unpredictable results because of nonstandard typecasts"
    )
    WIKI_RECOMMENDATION = "Use clear constants"

    def analyze_irs(self, irs: List[Operation]) -> List[Tuple[str, str]]:
        results = []
        for i in irs:
            try:
                if isinstance(i, TypeConversion):
                    from_type = i.variable.type
                    to_type = i.type

                    if not (is_ok_cast(str(from_type), str(to_type))):
                        results.append((from_type, to_type))
            except Exception as e:
                print("DubiousTypecast:Failed to check types", e)
                print(i)

        return results

    def get_dubious_typecasts(self, fun: FunctionContract, params=None):
        results: List[Tuple[Node, List[Tuple[str, str]]]] = []
        for node in fun.nodes:
            node_res = self.analyze_irs(node.irs)
            if node_res:
                results.append((node, node_res))
        return results

    def _detect(self):
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                func_res = self.get_dubious_typecasts(f)
                if func_res:
                    info = ["Dubious typecast in ", f, ":\n"]
                    for node, node_res in func_res:
                        for from_type, to_type in node_res:
                            info += [
                                f"\t{str(from_type)} => {str(to_type)} casting occurs in ",
                                node,
                                "\n",
                            ]
                    res = self.generate_result(info)
                    res.add(f)
                    results.append(res)

        return results
