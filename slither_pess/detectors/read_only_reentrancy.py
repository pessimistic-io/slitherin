""""
    Re-entrancy detection
    Based on heuristics, it may lead to FP and FN
    Iterate over all the nodes of the graph until reaching a fixpoint
"""
from collections import namedtuple, defaultdict
from typing import Dict, List, Set
from slither.core.variables.variable import Variable
from slither.core.declarations import Function
from slither.core.cfg.node import NodeType, Node, Contract
from slither.detectors.abstract_detector import DetectorClassification
from .reentrancy.reentrancy import (
    Reentrancy,
    to_hashable,
    AbstractState,
    union_dict,
    _filter_if,
    is_subset,
)
from slither.slithir.operations import EventCall

FindingKey = namedtuple("FindingKey", ["function", "calls"])
FindingValue = namedtuple("FindingValue", ["variable", "written_at", "node", "nodes"])


def are_same_contract(a: Contract, b: Contract) -> bool:
    """
    Checks if A==B or A inherits from B or otherwise
    """
    return a == b or (b in a.inheritance) or (b in a.derived_contracts)


class ReadOnlyReentrancyState(AbstractState):
    def __init__(self):
        super().__init__()
        self._reads_external: Dict[Variable, Set[Node]] = defaultdict(set)
        self._reads_external_contract_list: Dict[Variable, Set[Contract]] = defaultdict(
            set
        )
        self._written_external: Dict[Variable, Set[Node]] = defaultdict(set)
        self._written: Dict[Variable, Set[Node]] = defaultdict(set)

    @property
    def reads_external(self) -> Dict[Variable, Set[Node]]:
        return self._reads_external

    @property
    def reads_external_contract_list(self) -> Dict[Variable, Set[Contract]]:
        return self._reads_external_contract_list

    @property
    def written_external(self) -> Dict[Variable, Set[Node]]:
        return self._written_external

    @property
    def written(self) -> Dict[Variable, Set[Node]]:
        return self._written

    def add(self, fathers):
        super().add(fathers)
        self._reads_external = union_dict(self._reads_external, fathers.reads_external)
        self._reads_external_contract_list = union_dict(
            self._reads_external_contract_list, fathers.reads_external_contract_list
        )

    def does_not_bring_new_info(self, new_info):
        return (
            super().does_not_bring_new_info(new_info)
            and is_subset(new_info.reads_external, self._reads_external)
            and is_subset(
                new_info.reads_external_contract_list,
                self._reads_external_contract_list,
            )
        )

    def merge_fathers(self, node, skip_father, detector):
        for father in node.fathers:
            if detector.KEY in father.context:
                self._send_eth = union_dict(
                    self._send_eth,
                    {
                        key: values
                        for key, values in father.context[detector.KEY].send_eth.items()
                        if key != skip_father
                    },
                )
                self._calls = union_dict(
                    self._calls,
                    {
                        key: values
                        for key, values in father.context[detector.KEY].calls.items()
                        if key != skip_father
                    },
                )
                self._reads = union_dict(
                    self._reads, father.context[detector.KEY].reads
                )
                self._reads_external = union_dict(
                    self._reads_external, father.context[detector.KEY].reads
                )
                self._written_external = union_dict(
                    self._written_external, father.context[detector.KEY].reads
                )

    def analyze_node(self, node: Node, detector):
        state_vars_read: Dict[Variable, Set[Node]] = defaultdict(
            set, {v: {node} for v in node.state_variables_read}
        )

        # All the state variables written
        state_vars_written: Dict[Variable, Set[Node]] = defaultdict(
            set, {v: {node} for v in node.state_variables_written}
        )

        external_state_vars_read: Dict[Variable, Set[Node]] = defaultdict(set)
        external_state_vars_written: Dict[Variable, Set[Node]] = defaultdict(set)
        external_state_vars_read_contract_list: Dict[
            Variable, Set[Contract]
        ] = defaultdict(set)

        slithir_operations = []
        # Add the state variables written in internal calls
        for internal_call in node.internal_calls:
            # Filter to Function, as internal_call can be a solidity call
            if isinstance(internal_call, Function):
                for internal_node in internal_call.all_nodes():
                    for read in internal_node.state_variables_read:
                        state_vars_read[read].add(internal_node)
                    for write in internal_node.state_variables_written:
                        state_vars_written[write].add(internal_node)
                slithir_operations += internal_call.all_slithir_operations()

        for contract, v in node.high_level_calls:
            if isinstance(v, Function):
                for internal_node in v.all_nodes():
                    for read in internal_node.state_variables_read:
                        external_state_vars_read[read].add(internal_node)
                        external_state_vars_read_contract_list[read].add(contract)

                    if internal_node.context.get(detector.KEY):
                        for r in internal_node.context[detector.KEY].reads_external:
                            external_state_vars_read[r].add(internal_node)
                            external_state_vars_read_contract_list[r].add(contract)
                    for write in internal_node.state_variables_written:
                        external_state_vars_written[write].add(internal_node)

        contains_call = False

        self._written = state_vars_written
        self._written_external = external_state_vars_written
        for ir in node.irs + slithir_operations:
            if detector.can_callback(ir):
                self._calls[node] |= {ir.node}
                contains_call = True

            if detector.can_send_eth(ir):
                self._send_eth[node] |= {ir.node}

            if isinstance(ir, EventCall):
                self._events[ir] |= {ir.node, node}

        self._reads = union_dict(self._reads, state_vars_read)
        self._reads_external = union_dict(
            self._reads_external, external_state_vars_read
        )
        self._reads_external_contract_list = union_dict(
            self._reads_external_contract_list, external_state_vars_read_contract_list
        )

        return contains_call


class ReadOnlyReentrancy(Reentrancy):
    ARGUMENT = "pess-readonly-reentrancy"
    HELP = "Read-only reentrancy vulnerabilities"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = "https://github.com/pessimistic-io/slitherin/blob/master/docs/readonly_reentrancy.md"
    WIKI_TITLE = "Read-only reentrancy vulnerabilities"
    WIKI_DESCRIPTION = "Check docs"
    STANDARD_JSON = False
    KEY = "readonly_reentrancy"

    contracts_read_variable: Dict[Variable, Set[Contract]] = defaultdict(set)
    contracts_written_variable_after_reentrancy: Dict[
        Variable, Set[Contract]
    ] = defaultdict(set)

    def _explore(self, node, visited, skip_father=None):
        if node in visited:
            return

        visited = visited + [node]

        fathers_context = ReadOnlyReentrancyState()
        fathers_context.merge_fathers(node, skip_father, self)

        # Exclude path that dont bring further information
        if node in self.visited_all_paths:
            if self.visited_all_paths[node].does_not_bring_new_info(fathers_context):
                return
        else:
            self.visited_all_paths[node] = ReadOnlyReentrancyState()

        self.visited_all_paths[node].add(fathers_context)

        node.context[self.KEY] = fathers_context

        contains_call = fathers_context.analyze_node(node, self)
        node.context[self.KEY] = fathers_context

        sons = node.sons
        if contains_call and node.type in [NodeType.IF, NodeType.IFLOOP]:
            if _filter_if(node):
                son = sons[0]
                self._explore(son, visited, node)
                sons = sons[1:]
            else:
                son = sons[1]
                self._explore(son, visited, node)
                sons = [sons[0]]

        for son in sons:
            self._explore(son, visited)

    def find_writes_after_reentrancy(self):
        written_after_reentrancy: Dict[Variable, Set[Node]] = defaultdict(set)
        written_after_reentrancy_external: Dict[Variable, Set[Node]] = defaultdict(set)
        for contract in self.contracts:
            for f in contract.functions_and_modifiers_declared:
                for node in f.nodes:
                    # dead code
                    if self.KEY not in node.context:
                        continue
                    if node.context[self.KEY].calls:
                        if not any(n != node for n in node.context[self.KEY].calls):
                            continue
                        # TODO: check if written items exist
                        for v, nodes in node.context[self.KEY].written.items():
                            written_after_reentrancy[v].add(node)
                            self.contracts_written_variable_after_reentrancy[v].add(
                                contract
                            )
                        for v, nodes in node.context[self.KEY].written_external.items():
                            written_after_reentrancy_external[v].add(node)
                            self.contracts_written_variable_after_reentrancy[v].add(
                                contract
                            )

        return written_after_reentrancy, written_after_reentrancy_external

    # IMPORTANT:
    # FOR the external reads, that var should be external written in the same contract
    def get_readonly_reentrancies(self):
        (
            written_after_reentrancy,
            written_after_reentrancy_external,
        ) = self.find_writes_after_reentrancy()
        result = defaultdict(set)

        warnings = defaultdict(set)

        for contract in self.contracts:
            for f in contract.functions_and_modifiers_declared:
                for node in f.nodes:

                    if self.KEY not in node.context:
                        continue
                    vulnerable_variables = set()
                    warning_variables = set()
                    for r, nodes in node.context[self.KEY].reads.items():

                        if r in written_after_reentrancy:
                            finding_value = FindingValue(
                                r,
                                tuple(
                                    sorted(
                                        list(written_after_reentrancy[r]),
                                        key=lambda x: x.node_id,
                                    )
                                ),
                                node,
                                tuple(sorted(nodes, key=lambda x: x.node_id)),
                            )
                            if are_same_contract(r.contract, f.contract):
                                if f.view and f.visibility in ["public", "external"]:
                                    warning_variables.add(finding_value)
                            else:
                                vulnerable_variables.add(finding_value)

                    for r, nodes in node.context[self.KEY].reads_external.items():
                        if are_same_contract(r.contract, f.contract):
                            # TODO(yhtiyar): In case f.view we can notify the user that the given
                            # method could be vulnerable if other contract will use it
                            continue
                        if r in written_after_reentrancy_external:
                            isVulnerable = any(
                                c in self.contracts_written_variable_after_reentrancy[r]
                                for c in node.context[
                                    self.KEY
                                ].reads_external_contract_list[r]
                            )
                            if isVulnerable:
                                vulnerable_variables.add(
                                    FindingValue(
                                        r,
                                        tuple(
                                            sorted(
                                                list(
                                                    written_after_reentrancy_external[r]
                                                ),
                                                key=lambda x: x.node_id,
                                            )
                                        ),
                                        node,
                                        tuple(sorted(nodes, key=lambda x: x.node_id)),
                                    )
                                )

                        if r in written_after_reentrancy:
                            vulnerable_variables.add(
                                FindingValue(
                                    r,
                                    tuple(
                                        sorted(
                                            list(written_after_reentrancy[r]),
                                            key=lambda x: x.node_id,
                                        )
                                    ),
                                    node,
                                    tuple(sorted(nodes, key=lambda x: x.node_id)),
                                )
                            )

                    if vulnerable_variables:
                        finding_key = FindingKey(
                            function=f, calls=to_hashable(node.context[self.KEY].calls)
                        )
                        result[finding_key] |= vulnerable_variables
                    if warning_variables:
                        finding_key = FindingKey(
                            function=f, calls=to_hashable(node.context[self.KEY].calls)
                        )
                        warnings[finding_key] |= warning_variables
        return result, warnings

    def _gen_results(self, raw_results, info_text):
        results = []

        result_sorted = sorted(
            list(raw_results.items()), key=lambda x: x[0].function.name
        )

        varsRead: List[FindingValue]
        for (func, calls), varsRead in result_sorted:

            varsRead = sorted(varsRead, key=lambda x: (x.variable.name, x.node.node_id))

            info = [f"{info_text} ", func, ":\n"]

            info += [
                "\tState variables read that were written after the external call(s):\n"
            ]
            for finding_value in varsRead:
                info += [
                    "\t- ",
                    finding_value.variable,
                    " was read at ",
                    finding_value.node,
                    "\n",
                ]
                # info += ["\t- ", finding_value.node, "\n"]

                # for other_node in finding_value.nodes:
                #     if other_node != finding_value.node:
                #         info += ["\t\t- ", other_node, "\n"]

                # TODO: currently we are not printing the whole call-stack of variable
                # it wasn't working properly, so I am removing it for now to avoid confusion

                info += ["\t\t This variable was written at (after external call):\n"]
                for other_node in finding_value.written_at:
                    # info += ["\t- ", call_info, "\n"]
                    if other_node != finding_value.node:
                        info += ["\t\t\t- ", other_node, "\n"]

            # Create our JSON result
            res = self.generate_result(info)

            res.add(func)

            # Add all variables written via nodes which write them.
            for finding_value in varsRead:
                res.add(
                    finding_value.node,
                    {
                        "underlying_type": "variables_written",
                        "variable_name": finding_value.variable.name,
                    },
                )
                for other_node in finding_value.nodes:
                    if other_node != finding_value.node:
                        res.add(
                            other_node,
                            {
                                "underlying_type": "variables_written",
                                "variable_name": finding_value.variable.name,
                            },
                        )

            # Append our result
            results.append(res)

        return results

    def _detect(self):  # pylint: disable=too-many-branches
        results = []
        try:
            super()._detect()
            reentrancies, warnings = self.get_readonly_reentrancies()
            results += self._gen_results(reentrancies, "Readonly-reentrancy in ")
            results += self._gen_results(
                warnings,
                "Potential vulnerable to readonly-reentrancy function (if read in other function)",
            )
        except Exception as e:
            info = [
                "Error during detection of readonly-reentrancy:\n",
                "Please inform this to Yhtyyar\n",
                f"error details:",
                e,
            ]
        return results
