import argparse
import logging
from typing import List, Any, Optional
import subprocess
import os
import shutil
import pty
from pathlib import Path
import slither_pess
from pkg_resources import iter_entry_points

SLITHERIN_VERSION = "0.4.1"


def slitherin_detectors_list_as_arguments() -> str:
    return ",".join([detector.ARGUMENT for detector in slither_pess.plugin_detectors])


logging.basicConfig()
LOGGER = logging.getLogger("slitherinLogger")
LOGGER.setLevel(logging.INFO)

output_bytes = []


def read(fd):
    data = os.read(fd, 1024)
    output_bytes.append(data)
    return data


# this is modified version from : https://github.com/crytic/crytic-compile/blob/master/crytic_compile/utils/subprocess.py#L14
def run(
    cmd: List[str],
    **kwargs: Any,
) -> Optional[subprocess.CompletedProcess]:
    subprocess_cwd = Path(os.getcwd()).resolve()
    subprocess_exe = shutil.which(cmd[0])

    if subprocess_exe is None:
        LOGGER.error("Cannot execute `%s`, is it installed and in PATH?", cmd[0])
        return None

    LOGGER.info(
        "'%s' running (wd: %s)",
        " ".join(cmd),
        subprocess_cwd,
    )

    pty.spawn(cmd, read)  # this allows to print continuously and with colors


def handle_list() -> None:
    detectors = slither_pess.plugin_detectors
    for detector in detectors:
        print(detector.ARGUMENT)

    print("\nTo pass as argument (for --detect/--exclude):")
    print(slitherin_detectors_list_as_arguments())


def handle_parser(args: argparse.Namespace, slither_args) -> None:
    slitherin_detectors = slitherin_detectors_list_as_arguments()
    slither_with_args = ["slither"] + slither_args
    if args.pess:
        run(
            slither_with_args + ["--detect", slitherin_detectors],
        )
    elif args.slither:
        run(
            slither_with_args + ["--exclude", slitherin_detectors],
        )
    elif args.separated:
        print("Only slither results:")
        run(
            slither_with_args + ["--exclude", slitherin_detectors],
        )
        print("Only slitherin results:")
        run(
            slither_with_args + ["--ignore-compile", "--detect", slitherin_detectors],
        )
    else:
        run(slither_with_args)


def generate_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="""
        slitherin: Additional slither detectors by pessimistic.io
        All additional parameters will be passed to slither
        Usage examples:
            slitherin --pess PATH
            slitherin --pess PATH --json result.json
            slitherin --pess PATH --ignore-compile 
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"slitherin {SLITHERIN_VERSION}",
        help="Show version",
    )

    parser.add_argument(
        "--pess",
        action="store_true",
        help="Run only pessimistic.io (slitherin) detectors",
    )

    parser.add_argument(
        "--slither",
        action="store_true",
        help="Run only slither detectors",
    )

    parser.add_argument(
        "--separated",
        action="store_true",
        help="Run slither detectors, then slitherin",
    )
    return parser


def main() -> None:
    """
    Handler for the "slitherin" command.
    """

    parser = generate_argument_parser()
    parsed, unknown = parser.parse_known_args()

    # It turned out that argparse has no solution to parse unkown args and subcommands,
    # so u need to parse subcommands manually
    if unknown and unknown[0] == "list":
        handle_list()
        return
    if not unknown and not parsed._get_args():
        parser.print_help()
        return
    handle_parser(parsed, unknown)


if __name__ == "__main__":
    main()
