from slither.core.cfg.node import NodeType

from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


class UnprotectedSetter(AbstractDetector):
    """
    Sees if contract contains a setter, that changes contract paramater without modifier protection or access control inside the function
    """

    ARGUMENT = "pess-unprotected-setter"  # slither will launch the detector with slither.py --detect mydetector
    HELP = "Contract critical storage parameters might be changed by anyone"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_setter.md"
    WIKI_TITLE = "Unprotected Setter"
    WIKI_DESCRIPTION = "Usually all setters must be protected with access control"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Add access control"

    def is_setter(self, fun, params=None):
        if not params:
            params = fun.parameters
        for n in fun.nodes:
            if n.type == NodeType.EXPRESSION:
                for v in n.state_variables_written:
                    lr = str(n.expression).split(" = ")
                    if len(lr) > 1:
                        left = lr[0]
                        right = lr[1]
                        for p in params:
                            if p.name:
                                if "." in left:
                                    continue
                                if "[" in left:
                                    continue
                                if right == str(p):
                                    return left
        return None

    def has_access_control(self, fun):
        for m in fun.modifiers:
            for m.name in ["initializer", "onlyOwner"]:
                return True
        if fun.visibility in ["internal", "private"]:
            return True
        return fun.is_protected()

    def _detect(self):
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_interface:
                continue
            for f in contract.functions:
                if not self.has_access_control(f):
                    x = self.is_setter(f)
                    if x != None:
                        res.append(
                            self.generate_result(
                                [
                                    "Function",
                                    " ",
                                    f,
                                    " is a non-protected setter ",
                                    x,
                                    " is written" "\n",
                                ]
                            )
                        )
        return res
