import argparse
import logging
from typing import List, Any, Optional
import subprocess
import os
import shutil
from pathlib import Path
import slither_pess

SLITHERIN_VERSION = "0.4.0"


def slitherin_detectors_list_as_arguments() -> str:
    return ", ".join([detector.ARGUMENT for detector in slither_pess.plugin_detectors])


logging.basicConfig()
LOGGER = logging.getLogger("slitherinLogger")
LOGGER.setLevel(logging.INFO)


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

    try:
        process = subprocess.run(
            cmd,
            executable=subprocess_exe,
            cwd=subprocess_cwd,
            check=True,
            capture_output=True,
            text=True,
            **kwargs,
        )
        if process.stdout:
            print(process.stdout)
        if process.stderr:
            print(process.stderr)
    except FileNotFoundError:
        print(f"Could not execute {cmd[0]}, is it installed and in PATH?")
    except subprocess.CalledProcessError as e:
        print(f"{cmd[0]} returned non-zero exit code { e.returncode}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
    except OSError:
        print("OS error executing:", exc_info=True)


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
    elif args.seperated:
        print("Only slither results:")
        run(
            slither_with_args + ["--exclude", slitherin_detectors],
        )
        print("Only slitherin results:")
        run(
            slither_with_args + ["--detect", slitherin_detectors],
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
        "--seperated",
        action="store_true",
        help="Run slither detectors, then slitherin",
    )

    # parser.add_argument("slither-args", nargs=argparse.REMAINDER)

    # subcommands = parser.add_subparsers(dest="subcommands")

    # list_parser = subcommands.add_parser("list", help="List all slitherin detectors")
    # list_parser.set_defaults(func=handle_list)

    return parser


def main() -> None:
    """
    Handler for the "slitherin" command.
    """
    parser = generate_argument_parser()
    # parsed = parser.parse_args()
    parsed, unknown = parser.parse_known_args()

    if unknown and unknown[0] == "list":
        handle_list()
    if not unknown and not parsed._get_args():
        parser.print_help()
    handle_parser(parsed, unknown)


if __name__ == "__main__":
    main()
