import logging
from typing import Dict, List, Optional, Set

from slither.core.declarations import Contract
from slither.slithir.operations import EventCall
from slither.utils import output
from slither.utils.erc import ERC, ERC_EVENT
from slither.utils.type import (
    export_nested_types_from_variable,
    export_return_type_from_variable,
)


def generic_erc_checks(
    contract: Contract,
    erc_functions: List[ERC],
    erc_events: List[ERC_EVENT],
    ret: Dict[str, List],
    explored: Optional[Set[Contract]] = None,
) -> None:

    if explored is None:
        explored = set()

    explored.add(contract)

    logger.info(f"# Check {contract.name}\n")

    logger.info("## Check functions")
    for erc_function in erc_functions:
        _check_signature(erc_function, contract, ret)
    if erc_events:
        logger.info("\n## Check events")
        for erc_event in erc_events:
            _check_events(erc_event, contract, ret)

    logger.info("\n")

    for derived_contract in contract.derived_contracts:
        generic_erc_checks(derived_contract, erc_functions, erc_events, ret, explored)