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
from slither.detectors.reentrancy.reentrancy import (
    Reentrancy,
    to_hashable,
    AbstractState,
    union_dict,
    _filter_if,
    is_subset,
    dict_are_equal,
)
from slither.slithir.operations import Send, Transfer, EventCall
from slither.slithir.operations import Call

FindingKey = namedtuple("FindingKey", ["function", "calls", "send_eth"])
FindingValue = namedtuple("FindingValue", ["variable", "node", "nodes"])


class ReadOnlyReentrancyState(AbstractState):
    def __init__(self):
        super().__init__()
        self._reads_external: Dict[Variable, Set[Node]] = defaultdict(set)
        self._written_external: Dict[Variable, Set[Node]] = defaultdict(set)

    @property
    def reads_external(self) -> Dict[Variable, Set[Node]]:
        return self._reads_external

    @property
    def written_external(self) -> Dict[Variable, Set[Node]]:
        return self._written_external

    def add(self, fathers):
        super().add(fathers)
        self._reads_external = union_dict(self._reads_external, fathers.reads_external)

    def does_not_bring_new_info(self, new_info):
        return (
            super().does_not_bring_new_info(new_info)
            and dict_are_equal(self._reads_external, new_info.reads_external)
            and dict_are_equal(self._written_external, new_info.written_external)
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
                self._reads_prior_calls = union_dict(
                    self.reads_prior_calls,
                    father.context[detector.KEY].reads_prior_calls,
                )
                self._reads_external = union_dict(
                    self._reads_external, father.context[detector.KEY].reads_external
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
            print(f"External call to {contract.name}.{v.name}")
            for internal_node in v.all_nodes():
                for read in internal_node.state_variables_read:
                    print(f"External read of {contract.name}.{read}")
                    external_state_vars_read[read].add(internal_node)
                if internal_node.context[detector.KEY]:
                    for r in internal_node.context[detector.KEY].reads_external:
                        print(f"Secondarly External read of {contract.name}.{r}")
                        external_state_vars_read[r].add(internal_node)
                for write in internal_node.state_variables_written:
                    print(f"External write of {contract.name}.{write}")
                    external_state_vars_written[write].add(internal_node)

        contains_call = False

        self._written = state_vars_written
        self._written_external = external_state_vars_written
        for ir in node.irs + slithir_operations:
            if detector.can_callback(ir):
                self._calls[node] |= {ir.node}
                self._reads_prior_calls[node] = set(
                    self._reads_prior_calls.get(node, set())
                    | set(node.context[detector.KEY].reads.keys())
                    | set(state_vars_read.keys())
                )
                contains_call = True

            if detector.can_send_eth(ir):
                self._send_eth[node] |= {ir.node}

            if isinstance(ir, EventCall):
                self._events[ir] |= {ir.node, node}

        self._reads = union_dict(self._reads, state_vars_read)
        self._reads_external = union_dict(
            self._reads_external, external_state_vars_read
        )

        return contains_call


class ReadOnlyReentrancy(Reentrancy):
    ARGUMENT = "readonly-reentrancy"
    HELP = "Read-only reentrancy vulnerabilities"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/crytic/slither/wiki/Detector-Documentation#reentrancy-vulnerabilities-2"

    WIKI_TITLE = "Read-only reentrancy vulnerabilities"

    # region wiki_description
    WIKI_DESCRIPTION = """
Detection of the [reentrancy bug](https://github.com/trailofbits/not-so-smart-contracts/tree/master/reentrancy).
Only report reentrancy that acts as a double call (see `reentrancy-eth`, `reentrancy-no-eth`)."""
    # endregion wiki_description

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """
```solidity
    function callme(){
        if( ! (msg.sender.call()() ) ){
            throw;
        }
        counter += 1
    }   
```
`callme` contains a reentrancy. The reentrancy is benign because it's exploitation would have the same effect as two consecutive calls."""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = "Apply the [`check-effects-interactions` pattern](http://solidity.readthedocs.io/en/v0.4.21/security-considerations.html#re-entrancy)."

    STANDARD_JSON = False

    vulnarable_functions: Dict[Function, Set[Variable]] = defaultdict(set)
    externally_written_in: Dict[Variable, Set[Contract]] = defaultdict(set)

    def _explore(self, node, visited, skip_father=None):
        """
        Explore the CFG and look for re-entrancy
        Heuristic: There is a re-entrancy if a state variable is written
                    after an external call

        node.context will contains the external calls executed
        It contains the calls executed in father nodes

        if node.context is not empty, and variables are written, a re-entrancy is possible
        """
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
        written_after_reentrancy: Dict[Variable, List[Function]] = defaultdict(list)
        written_after_reentrancy_external: Dict[Variable, List[Function]] = defaultdict(
            list
        )
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
                            written_after_reentrancy[v].append(nodes)
                        for v, nodes in node.context[self.KEY].written_external.items():
                            written_after_reentrancy_external[v].append(nodes)
                            self.externally_written_in[v].add(contract)

        return written_after_reentrancy, written_after_reentrancy_external

    def _explore_functions(self, function, visited):
        if function in visited:
            return
        print("WTF")
        visited.add(function)
        for node in function.nodes:
            if self.KEY not in node.context:
                continue
            if node.context[self.KEY].calls:
                for c in node.context[self.KEY].calls:
                    print(f"{function.name} calls {c}")
                    # self._explore(c.function, visited)

        pass

    # IMPORTANT:
    # FOR the external reads, that war should be external written in the same contract
    def get_readonly_reentrancies(self):
        (
            written_after_reentrancy,
            written_after_reentrancy_external,
        ) = self.find_writes_after_reentrancy()
        for contract in self.contracts:
            for f in contract.functions_and_modifiers_declared:
                # if not f.view:
                #     continue
                for node in f.nodes:

                    if self.KEY not in node.context:
                        continue
                    if contract.name == "SecondaryVictim":
                        for r, _ in node.context[self.KEY].reads.items():
                            print(f"SECONDARY VICTIM READ {r}")
                    for r, nodes in node.context[self.KEY].reads.items():
                        if r.contract == f.contract and not f.view:
                            continue

                        if r in written_after_reentrancy:
                            print(
                                f"{f.name} is vulnerable, reads {r}, which is written after reentrancy"
                            )

                    for r, nodes in node.context[self.KEY].reads_external.items():
                        if r in written_after_reentrancy_external:
                            print(
                                f"{f.name} is vulnerable, external reads {r}, which is external written after reentrancy"
                            )
                        if r in written_after_reentrancy:
                            print(
                                f"{f.name} is vulnerable, external reads {r}, which is written after reentrancy"
                            )

    def _detect(self):  # pylint: disable=too-many-branches
        """"""

        super()._detect()
        reentrancies = self.get_readonly_reentrancies()

        results = []

        # # result_sorted = sorted(
        # #     list(reentrancies.items()), key=lambda x: x[0].function.name
        # # )
        # print(f"result_sorted: {result_sorted}")
        return []
        varsWritten: List[FindingValue]
        for (func, calls, send_eth), varsWritten in result_sorted:
            calls = sorted(list(set(calls)), key=lambda x: x[0].node_id)
            send_eth = sorted(list(set(send_eth)), key=lambda x: x[0].node_id)
            varsWritten = sorted(
                varsWritten, key=lambda x: (x.variable.name, x.node.node_id)
            )

            info = ["Reentrancy in ", func, ":\n"]

            info += ["\tExternal calls:\n"]
            for (call_info, calls_list) in calls:
                info += ["\t- ", call_info, "\n"]
                for call_list_info in calls_list:
                    if call_list_info != call_info:
                        info += ["\t\t- ", call_list_info, "\n"]
            if calls != send_eth and send_eth:
                info += ["\tExternal calls sending eth:\n"]
                for (call_info, calls_list) in send_eth:
                    info += ["\t- ", call_info, "\n"]
                    for call_list_info in calls_list:
                        if call_list_info != call_info:
                            info += ["\t\t- ", call_list_info, "\n"]
            info += ["\tState variables written after the call(s):\n"]
            for finding_value in varsWritten:
                info += ["\t- ", finding_value.node, "\n"]
                for other_node in finding_value.nodes:
                    if other_node != finding_value.node:
                        info += ["\t\t- ", other_node, "\n"]

            # Create our JSON result
            res = self.generate_result(info)

            # Add the function with the re-entrancy first
            res.add(func)

            # Add all underlying calls in the function which are potentially problematic.
            for (call_info, calls_list) in calls:
                res.add(call_info, {"underlying_type": "external_calls"})
                for call_list_info in calls_list:
                    if call_list_info != call_info:
                        res.add(
                            call_list_info,
                            {"underlying_type": "external_calls_sending_eth"},
                        )

            #

            # If the calls are not the same ones that send eth, add the eth sending nodes.
            if calls != send_eth:
                for (call_info, calls_list) in calls:
                    res.add(
                        call_info, {"underlying_type": "external_calls_sending_eth"}
                    )
                    for call_list_info in calls_list:
                        if call_list_info != call_info:
                            res.add(
                                call_list_info,
                                {"underlying_type": "external_calls_sending_eth"},
                            )

            # Add all variables written via nodes which write them.
            for finding_value in varsWritten:
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
