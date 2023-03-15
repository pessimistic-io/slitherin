import argparse
from collections import defaultdict
from typing import Dict, List

from crytic_compile import cryticparser
from slither import Slither


PROJECTS = {"Uniswap_V2": uniswap_v2}


def parse_args() -> argparse.Namespace:
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    parser = argparse.ArgumentParser(
        description="Check integration with projects",
        usage="pess-slither-integration filename",
    )

    parser.add_argument("project", help="The target directory/Solidity file.")

    parser.add_argument(
        "contract_name",
        help="The name of the contract. Specify the first case contract that follow the standard. Derived contracts will be checked.",
    )

    parser.add_argument(
        "--project",
        help=f"Project integration with which is to be checked, available {PROJECTS}",
        action="store",
    )

    parser.add_argument(
        "--json",
        help='Export the results as a JSON file ("--json -" to export to stdout)',
        action="store",
        default=False,
    )

    # Add default arguments from crytic-compile
    cryticparser.init(parser)

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Perform slither analysis on the given filename
    slither = Slither(args.project, **vars(args))

    ret: Dict[str, List] = defaultdict(list)

    contracts = slither.get_contract_from_name(args.contract_name)

    contract = contracts[0]

    generic_erc_checks(contract, PROJECTS[0], ret) # change function name on actual

    if args.json:
        output_to_json(args.json, None, {"integration-check": ret})


if __name__ == "__main__":
    main()