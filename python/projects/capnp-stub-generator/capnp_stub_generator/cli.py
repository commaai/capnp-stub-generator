"""Command-line interface for generating type hints for *.capnp schemas.

Notes:
    - This generator requires pycapnp >= 1.0.0.
    - Capnp interfaces (RPC) are not yet supported.
"""

from __future__ import annotations

import argparse
import logging
import os.path
from typing import Sequence

from capnp_stub_generator.generator import run

logger = logging.getLogger(__name__)


def _add_output_argument(parser: argparse.ArgumentParser):
    """Add an output argument to a parser.

    Args:
        parser (argparse.ArgumentParser): The parser to add the argument to.
    """
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        default=None,
        help="override directory where to write the .pyi file",
    )


def _add_recursive_argument(parser: argparse.ArgumentParser):
    """Add a recursive argument to a parser.

    Args:
        parser (argparse.ArgumentParser): The parser to add the argument to.
    """
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        default=False,
        action="store_true",
        help="recursively search for *.capnp files with a given glob expression.",
    )


def setup_parser() -> argparse.ArgumentParser:
    """Setup for the parser.

    Returns:
        argparse.ArgumentParser: The parser after setup.
    """
    parser = argparse.ArgumentParser(description="Generate type hints for capnp schema files.")

    parser.add_argument(
        "-p",
        "--paths",
        type=str,
        nargs="+",
        default=["**/*.capnp"],
        help="path or glob expressions that match *.capnp files.",
    )

    parser.add_argument(
        "-e",
        "--excludes",
        type=str,
        nargs="+",
        default=["**/c-capnproto/**/*.capnp"],
        help="path or glob expressions to exclude from matches.",
    )

    _add_output_argument(parser)
    _add_recursive_argument(parser)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point of the stub generator.

    Args:
        argv (Sequence[str] | None, optional): Run arguments. Defaults to None.

    Returns:
        int: Error code.
    """
    logging.basicConfig(level=logging.INFO)

    root_directory = os.getcwd()
    logging.info("Working from root directory: %s", root_directory)

    parser = setup_parser()
    args = parser.parse_args(argv)

    run(args, root_directory)

    return 0


if __name__ == "__main__":
    main(
        [
            "-p",
            "python/libraries/mars/mars/interfaces/**/*.capnp",
            "-r",
        ]
    )
