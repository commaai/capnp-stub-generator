"""Top-level module for stub generation."""

from __future__ import annotations

import argparse
import glob
import logging
import os.path
from types import ModuleType
from typing import Set

import black
import capnp
import isort
from capnp_stub_generator.capnp_types import ModuleRegistryType
from capnp_stub_generator.helper import replace_capnp_suffix
from capnp_stub_generator.writer import Writer

capnp.remove_import_hook()


logger = logging.getLogger(__name__)

PYI_SUFFIX = ".pyi"
PY_SUFFIX = ".py"


def generate_stubs(module: ModuleType, module_registry: ModuleRegistryType, output_file_path: str):
    """Entry-point for generating *.pyi stubs from a module definition.

    Args:
        module (ModuleType): The module to generate stubs for.
        module_registry (ModuleRegistryType): A registry of all detected modules.
        output_file_path (str): The name of the output stub files, without file extension.
    """
    writer = Writer(module, module_registry)
    writer.generate_recursive()

    for outputs, suffix in zip((writer.dumps_pyi(), writer.dumps_py()), (PYI_SUFFIX, PY_SUFFIX)):
        sorted_imports = isort.code(outputs, config=isort.Config(profile="black"))
        formatted_output = black.format_str(sorted_imports, mode=black.Mode(is_pyi=True, line_length=79))

        with open(output_file_path + suffix, "w", encoding="utf8") as output_file:
            output_file.write(formatted_output)

    logger.info("Wrote stubs to '%s(%s/%s)'.", output_file_path, PYI_SUFFIX, PY_SUFFIX)


def run(args: argparse.Namespace, root_directory: str):
    """Run the stub generator on a set of paths that point to *.capnp schemas.

    Uses `generate_stubs` on each input file.

    Args:
        args (argparse.Namespace): The arguments that were passed when calling the stub generator.
        root_directory (str): The directory, from which the generator is executed.
    """
    paths: str = args.paths
    excludes: str = args.excludes

    excluded_paths: Set[str] = set()
    for exclude in excludes:
        exclude_directory = os.path.join(root_directory, exclude)
        excluded_paths = excluded_paths.union(glob.glob(exclude_directory, recursive=args.recursive))

    search_paths: Set[str] = set()
    for path in paths:
        search_directory = os.path.join(root_directory, path)
        search_paths = search_paths.union(glob.glob(search_directory, recursive=args.recursive))

    # The `valid_paths` contain the automatically detected search paths, except for specifically excluded paths.
    valid_paths = search_paths - excluded_paths

    parser = capnp.SchemaParser()
    module_registry: ModuleRegistryType = {}

    for path in valid_paths:
        module = parser.load(path)
        module_registry[module.schema.node.id] = (path, module)

    for path, module in module_registry.values():
        output_directory = os.path.dirname(path)
        output_file_name = replace_capnp_suffix(os.path.basename(path))

        generate_stubs(module, module_registry, os.path.join(output_directory, output_file_name))
