import argparse
import logging
from typing import List, Any, Optional
import subprocess
import os
import shutil
import pty
import sys
from pathlib import Path
import slitherin
from pkg_resources import iter_entry_points

from .consts import *


def slitherin_detectors_list_as_arguments() -> str:
    return ",".join([detector.ARGUMENT for detector in slitherin.plugin_detectors])


def arbitrum_detectors_list_as_arguments() -> str:
    return ",".join([detector.ARGUMENT for detector in slitherin.artbitrum_detectors])


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

    master, slave = pty.openpty()

    try:
        process = subprocess.Popen(cmd, stdout=slave, stderr=slave, text=False)
        os.close(slave)

        while True:
            try:
                output = os.read(master, 1024)
            except OSError as e:
                if e.errno == 5:  # Errno 5 corresponds to Input/output error
                    break
                else:
                    raise
            if not output:
                break
            decoded_output = output.decode(sys.stdout.encoding, errors="replace")
            print(decoded_output, end="")

        return_code = process.wait()
        if return_code != 0:
            raise Exception(
                f"Errored out with code: {return_code}, while running slither"
            )

    except Exception as e:
        print(f"Failed to run slither: {str(e)}")
        raise e


def handle_list() -> None:
    detectors = slitherin.plugin_detectors
    for detector in detectors:
        print(detector.ARGUMENT)

    print("\nTo pass as argument (for --detect/--exclude):")
    print(slitherin_detectors_list_as_arguments())


def handle_parser(args: argparse.Namespace, slither_args) -> None:
    slitherin_detectors = slitherin_detectors_list_as_arguments()
    slither_with_args = [
        "slither",
        "--fail-none",
    ] + slither_args  # using fail-none flag, so slither will return 0 even though there are findings

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
    elif args.arbitrum:
        os.environ["SLITHERIN_ARBITRUM"] = "True"
        run(slither_with_args + ["--detect", arbitrum_detectors_list_as_arguments()])
        del os.environ["SLITHERIN_ARBITRUM"]

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

    parser.add_argument(
        "--arbitrum",
        action="store_true",
        help="Run arbitrum detectors",
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
