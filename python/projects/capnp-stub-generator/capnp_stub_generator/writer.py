"""Generate type hints for *.capnp schemas.

Note: This generator requires pycapnp >= 1.0.0.

Note: capnp interfaces (RPC) are not yet supported.
"""

from __future__ import annotations

import dataclasses
import keyword
import logging
import os.path
import pathlib
from types import ModuleType
from typing import Any, Literal, Set

import capnp
from capnp_stub_generator.capnp_types import (
    CAPNP_TYPE_TO_PYTHON,
    CapnpElementType,
    CapnpFieldType,
    CapnpSlotType,
    ModuleRegistryType,
)
from capnp_stub_generator.helper import replace_capnp_suffix

capnp.remove_import_hook()


logger = logging.getLogger(__name__)

INDENT_SPACES = 4


class NoParentError(Exception):
    """Raised, when the parent of a scope is not available."""


@dataclasses.dataclass
class Scope:
    """A scope within the output .pyi file.

    Scopes contain text and are indented by a certain amount. They often have parents, within which they are located.

    Args:
        name (str): The name of the scope. Use an empty name for the root scope ("").
        id (int): A numerical identifier of the scope.
        parent (Scope | None): The direct parent scope of this scope, if there is any.
        return scope (Scope | None): The scope to which to return, when closing this one.
        lines (list[str]): The list of text lines in this scope.
    """

    name: str
    id: int
    parent: Scope | None
    return_scope: Scope | None
    lines: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        """Assures that, if this is the root scope, its name is empty."""
        assert (self.is_root) == (self.name == "")

    @property
    def parents(self) -> list[Scope]:
        """A list of all parent scopes of this scope, starting from the first parent.

        If the returned list is empty, this scope has no parents. The first parent in the list has no further
        parents, it is the root scope.
        """
        parents: list[Scope] = []
        scope: Scope | None = self.parent

        while scope is not None:
            parents.append(scope)
            scope = scope.parent

        parents.reverse()

        return parents

    @property
    def trace(self) -> list[Scope]:
        """A list of all scopes that lead to this scope, starting from the first parent.

        The first parent has no further parents.
        """
        return self.parents + [self]

    @property
    def root(self) -> Scope:
        """Get the root scope that has no further parents."""
        if not self.parents:
            return self

        else:
            return self.parents[0]

    @property
    def is_root(self) -> bool:
        """Determine, whether this is the root scope."""
        return self.root == self

    @property
    def indent_spaces(self) -> int:
        """The number of spaces by which this scope is indented."""
        return len(self.parents) * INDENT_SPACES

    def add_line(self, line: str = ""):
        """Add a line to this scope, taking into account the current indent spaces.

        Args:
            line (str): The line to add. Optional, defaults to "".
        """
        if not line:
            self.lines.append("")

        else:
            self.lines.append(" " * self.indent_spaces + line)

    def trace_as_str(self, delimiter: Literal[".", "_"] = ".") -> str:
        """A string representation of this scope's relative trace.

        Follow the trace of the scope, and connect parent scopes with a delimiter.
        The root scope is not included in this trace string.

        Args:
            delimiter (Literal[".", "_"]): The delimiter to join the scope names with.
        """
        return delimiter.join((scope.name for scope in self.trace if not scope.is_root))

    def __repr__(self) -> str:
        """A string representation of this scope.

        Follow the path of scopes, and connect parent scopes with '.'.
        """
        return self.trace_as_str(".")


@dataclasses.dataclass
class CapnpType:
    """Represents a type that is extracted from a .capnp schema.

    Args:
        schema (Any):
        name (str):
        scope (Scope):
        generic_params (list[str]):
    """

    schema: Any
    name: str
    scope: Scope
    generic_params: list[str] = dataclasses.field(default_factory=list)


class Writer:
    """A class that handles writing the stub file, based on a provided module definition."""

    VALID_TYPING_IMPORTS = Literal["Generic", "TypeVar", "List", "Literal", "Union", "overload"]

    def __init__(self, module: ModuleType, module_registry: ModuleRegistryType):
        """Initialize the stub writer with a module definition.

        Args:
            module (ModuleType): The module definition to parse and write a stub for.
            module_registry (ModuleRegistryType): The module registry, for finding dependencies between loaded modules.
        """
        self.scope = Scope(name="", id=module.schema.node.id, parent=None, return_scope=None)
        self.scopes_by_id: dict[int, Scope] = {self.scope.id: self.scope}

        self._module = module
        self._module_registry = module_registry

        if self._module.__file__:
            self._module_path = pathlib.Path(self._module.__file__)

        else:
            raise ValueError("The module has no file path attached to it.")

        self._imports: Set[str] = set()
        self._add_import("from __future__ import annotations")

        self._typing_imports: Set[Writer.VALID_TYPING_IMPORTS] = set()

        self.type_vars: set[str] = set()
        self.type_map: dict[int, CapnpType] = {}

        self.docstring = f'"""This is an automatically generated stub for `{self._module_path.name}`."""'

    def _add_typing_import(self, module_name: Writer.VALID_TYPING_IMPORTS):
        """Add an import for a module from the 'typing' package.

        E.g., when using
        add_typing_import("List")
        add_typing_import("Union")

        this generates an import line `from typing import List, Union`.

        Args:
            module_name (Writer.VALID_TYPING_IMPORTS): The module to import from `typing`.
        """
        self._typing_imports.add(module_name)

    def _add_import(self, import_line: str):
        """Add a full import line.

        E.g. 'import numpy as np'.

        Args:
            import_line (str): The import line to add.
        """
        self._imports.add(import_line)

    def _add_enum_import(self):
        """Adds an import for the `Enum` class."""
        self._add_import("from enum import Enum")

    @property
    def base_module_name(self) -> str:
        """The base name of this writer's target module."""
        return self._module.schema.node.displayName

    @property
    def imports(self) -> list[str]:
        """Get the full list of import strings that were added to the writer, including typing imports.

        Returns:
            list[str]: The list of imports that were previously added.
        """
        import_lines: list[str] = []

        for imp in self._imports:
            import_lines.append(imp)

        if self._typing_imports:
            import_lines.append("from typing import " + ", ".join(sorted(self._typing_imports)))

        return import_lines

    @staticmethod
    def get_display_name(schema: Any) -> str:
        """Extract the display name from the schema.

        Args:
            schema (Any): The schema to get the display name from.

        Returns:
            str: The display name of the schema.
        """
        return schema.node.displayName[schema.node.displayNamePrefixLength :]

    def gen_const(self, schema: Any) -> None:
        """Generate a `const` object.

        Args:
            schema (Any): The schema to generate the `const` object out of.
        """
        assert schema.node.which() == CapnpElementType.CONST

        name = self.get_display_name(schema)
        python_type = CAPNP_TYPE_TO_PYTHON[schema.node.const.type.which()]
        self.scope.add_line(f"{name}: {python_type}")

    def gen_enum(self, schema: Any) -> CapnpType | None:
        """Generate an `enum` object.

        Args:
            schema (Any): The schema to generate the `enum` object out of.
        """
        assert schema.node.which() == CapnpElementType.ENUM

        imported = self.register_import(schema)

        if imported is not None:
            return imported

        name = self.get_display_name(schema)
        self._add_enum_import()

        self.new_scope(name, schema.node, f"class {name}(str, Enum):")
        self.register_type(schema.node.id, schema, name)

        for enumerant in schema.node.enum.enumerants:
            value = enumerant.name
            name = enumerant.name

            if enumerant.name in keyword.kwlist:
                # Avoid naming collisions with Python keywords.
                name += "_"

            self.scope.add_line(f'{name}: str = "{value}"')

        self.return_from_scope()

        return None

    def gen_generic(self, schema: Any) -> list[str]:
        """Generate a `generic` type variable.

        Args:
            schema (Any): The schema to generate the `generic` object out of.

        Returns:
            list[str]: The list of registered generic type variables.
        """
        self._add_typing_import("TypeVar")
        self._add_typing_import("Generic")

        generic_params: list[str] = [param.name for param in schema.node.parameters]
        referenced_params: list[str] = []

        for field, _ in zip(schema.node.struct.fields, schema.as_struct().fields_list):
            if field.slot.type.which() == "anyPointer" and field.slot.type.anyPointer.which() == "parameter":
                param = field.slot.type.anyPointer.parameter

                t = self.get_type_by_id(param.scopeId)

                if t is not None:
                    param_source = t.schema
                    source_params: list[str] = [param.name for param in param_source.node.parameters]
                    referenced_params.append(source_params[param.parameterIndex])

        return [self.register_type_var(param) for param in generic_params + referenced_params]

    def gen_slot(
        self,
        schema: Any,
        field: Any,
        raw_field: Any,
        registered_type: CapnpType,
        contructor_kwargs: list[str],
        init_choices: list[tuple[str, str]],
    ) -> None:
        """Generate a slot of a type that is yet to be determined.

        Args:
            schema (Any): The schema to extract the slot from.
            field (Any): FIXME
            raw_field (Any): FIXME
            registered_type (Type): FIXME
            contructor_kwargs (list[str]): FIXME
            init_choices (list[tuple[str, str]]): FIXME
        """

        def gen_list_slot():
            """Generate a slot, which contains a `list`."""
            list_slot_type: CapnpElementType = field.slot.type.list.elementType.which()

            if list_slot_type == CapnpElementType.STRUCT:
                if not self.is_type_id_known(field.slot.type.list.elementType.struct.typeId):
                    self.generate_nested(raw_field.schema.elementType)

            elif list_slot_type == CapnpElementType.ENUM:
                if not self.is_type_id_known(field.slot.type.list.elementType.enum.typeId):
                    self.generate_nested(raw_field.schema.elementType)

            type_name = self.get_type_name(field.slot.type.list.elementType)
            field_py_code = f"{field.name}: List[{type_name}]"
            self.scope.add_line(field_py_code)
            contructor_kwargs.append(field_py_code)
            self._add_typing_import("List")

        def gen_python_type_slot():
            """Generate a slot, which contains a regular Python type."""
            python_type_name: str = CAPNP_TYPE_TO_PYTHON[field_slot_type]

            field_py_code = f"{field.name}: {python_type_name}"
            self.scope.add_line(field_py_code)
            contructor_kwargs.append(field_py_code)

        def gen_enum_slot():
            """Generate a slot, which contains an `enum`."""
            if not self.is_type_id_known(field.slot.type.enum.typeId):
                try:
                    self.generate_nested(raw_field.schema)

                except NoParentError:
                    pass

            type_name = self.get_type_name(field.slot.type)
            field_py_code = f"{field.name}: {type_name}"
            self.scope.add_line(field_py_code)
            contructor_kwargs.append(field_py_code)

        def gen_struct_slot():
            """Generate a slot, which contains a `struct`."""
            elem_type = raw_field.schema

            if not self.is_type_id_known(elem_type.node.id):
                self.gen_struct(elem_type)

            type_name = self.get_type_name(field.slot.type)
            field_py_code = f"{field.name}: {type_name}"
            self.scope.add_line(field_py_code)
            contructor_kwargs.append(field_py_code)
            init_choices.append((field.name, type_name))

        def gen_any_pointer_slot():
            """Generate a slot, which contains an `any_pointer` object."""
            param = field.slot.type.anyPointer.parameter
            type_name = registered_type.generic_params[param.parameterIndex]
            field_py_code = f"{field.name}: {type_name}"
            self.scope.add_line(field_py_code)
            contructor_kwargs.append(field_py_code)

        field_slot_type = field.slot.type.which()

        if field_slot_type == CapnpSlotType.LIST:
            gen_list_slot()

        elif field_slot_type in CAPNP_TYPE_TO_PYTHON:
            gen_python_type_slot()

        elif field_slot_type == CapnpSlotType.ENUM:
            gen_enum_slot()

        elif field_slot_type == CapnpSlotType.STRUCT:
            gen_struct_slot()

        elif field_slot_type == CapnpSlotType.ANY_POINTER:
            gen_any_pointer_slot()

        else:
            raise AssertionError(f"{schema.node.displayName}: {field.name}: " f"{field_slot_type}")

    def gen_struct(self, schema: Any, type_name: str = "") -> CapnpType:
        """Generate a `struct` object.

        Args:
            schema (Any): The schema to generate the `struct` object out of.
            type_name (str, optional): A type name to override the display name of the struct. Defaults to "".

        Returns:
            Type: The `struct`-type module that was generated.
        """
        assert schema.node.which() == CapnpElementType.STRUCT

        imported = self.register_import(schema)

        if imported is not None:
            return imported

        if not type_name:
            type_name = self.get_display_name(schema)

        registered_params: list[str] = []
        if schema.node.isGeneric:
            registered_params = self.gen_generic()

        if registered_params:
            scope_decl_line = f"class {type_name}(Generic[{', '.join(registered_params)}]):"

        else:
            scope_decl_line = f"class {type_name}:"

        self.new_scope(type_name, schema.node, scope_decl_line)

        registered_type: CapnpType = self.register_type(schema.node.id, schema, name=type_name)
        registered_type.generic_params = registered_params
        type_name = registered_type.name
        definition_has_body = False

        init_choices: list[tuple[str, str]] = []
        contructor_kwargs: list[str] = []

        for field, raw_field in zip(schema.node.struct.fields, schema.as_struct().fields_list):
            field_type = field.which()

            if field_type == CapnpFieldType.SLOT:
                definition_has_body = True
                self.gen_slot(schema, field, raw_field, registered_type, contructor_kwargs, init_choices)

            elif field_type == CapnpFieldType.GROUP:
                group_name = field.name[0].upper() + field.name[1:]

                assert group_name != field.name

                raw_schema = raw_field.schema
                group_name = self.gen_struct(raw_schema, type_name=group_name).name
                field_py_code = f"{field.name}: {group_name}"
                self.scope.add_line(field_py_code)
                contructor_kwargs.append(field_py_code)
                definition_has_body = True
                init_choices.append((field.name, group_name))

            else:
                raise AssertionError(f"{schema.node.displayName}: {field.name}: " f"{field.which()}")

        if not registered_type.scope.is_root:
            scoped_name = f"{registered_type.scope}.{type_name}"

        else:
            scoped_name = type_name

        self.scope.add_line("@staticmethod")
        self.scope.add_line(f"def from_bytes(data: bytes) -> {scoped_name}: ...")
        self.scope.add_line("def to_bytes(self) -> bytes: ...")
        definition_has_body = True

        if schema.node.struct.discriminantCount:
            literals = ", ".join(
                f'Literal["{field.name}"]' for field in schema.node.struct.fields if field.discriminantValue != 65535
            )
            self._add_typing_import("Literal")
            self._add_typing_import("Union")
            self.scope.add_line(f"def which(self) -> Union[{literals}]: ...")
            definition_has_body = True

        if contructor_kwargs:
            kwargs = ", ".join(f"{kwarg} = ..." for kwarg in contructor_kwargs)
            self.scope.add_line(f"def __init__(self, *, {kwargs}) -> None: ...")
            definition_has_body = True

        if len(init_choices) > 1:
            self._add_typing_import("Literal")
            self._add_typing_import("overload")

            for field_name, field_type in init_choices:

                self.scope.add_line("@overload")
                self.scope.add_line(f'def init(self, name: Literal["{field_name}"])' f" -> {field_type}: ...")

        elif len(init_choices) == 1:
            self._add_typing_import("Literal")
            field_name, field_type = init_choices[0]
            self.scope.add_line(f'def init(self, name: Literal["{field_name}"])' f" -> {field_type}: ...")

        if not definition_has_body:
            self.scope.add_line("pass")

        self.return_from_scope()

        return registered_type

    def generate_nested(self, schema: Any) -> None:
        """Generate the type for a nested schema.

        Args:
            schema (Any): The schema to generate types for.

        Raises:
            AssertionError: If the schema belongs to an unknown type.
        """
        if schema.node.id in self.type_map:
            return  # already generated type hints for this type

        node_type = schema.node.which()

        if node_type == "const":
            self.gen_const(schema)

        elif node_type == "struct":
            self.gen_struct(schema)

        elif node_type == "enum":
            self.gen_enum(schema)

        elif node_type == "interface":
            logger.warning("Skipping interface: not implemented")

        else:
            raise AssertionError(node_type)

    def generate_recursive(self):
        """Generate types for all nested nodes, recursively."""
        for node in self._module.schema.node.nestedNodes:
            self.generate_nested(self._module.schema.get_nested(node.name))

    def register_import(self, schema) -> CapnpType | None:
        """Determine, whether a schema is imported from the base module.

        If so, the type definition that the schema contains, is added to the type registry.

        Args:
            schema (Any): The schema to check.

        Returns:
            Type | None: The type of the import, if the schema is imported,
                or None if the schema defines the base module itself.
        """
        module_name, definition_name = schema.node.displayName.split(":")

        if module_name == self.base_module_name:
            # This is the base module, not an import.
            return None

        common_path: str
        matching_path: pathlib.Path | None = None

        # Find the path of the parent module, from which this schema is imported.
        for path, module in self._module_registry.values():
            for node in module.schema.node.nestedNodes:
                if node.id == schema.node.id:
                    matching_path = pathlib.Path(path)
                    break

        # Since this is an import, there must be a parent module.
        assert matching_path is not None

        # Find the relative path to go from the parent module, to this imported module.
        common_path = os.path.commonpath([self._module_path, matching_path])

        relative_module_path = self._module_path.relative_to(common_path)
        relative_import_path = matching_path.relative_to(common_path)

        # Shape the relative path to a relative Python import statement.
        python_import_path = "." * len(relative_module_path.parents) + replace_capnp_suffix(
            ".".join(relative_import_path.parts)
        )
        self._add_import(f"from {python_import_path} import {definition_name}")

        return self.register_type(schema.node.id, schema, name=definition_name, scope=self.scope.root)

    def register_type_var(self, name: str) -> str:
        """Find and register the full name of a type variable, which includes its scopes.

        Args:
            name (str): The type name to register.

        Returns:
            str: The full name in the format scope0_scope1_..._scopeN_name, including the type name to register.
        """
        full_name: str = self.scope.trace_as_str("_") + f"_{name}"

        self.type_vars.add(full_name)
        return full_name

    def register_type(self, type_id: int, schema: Any, name: str = "", scope: Scope | None = None) -> CapnpType:
        """Register a new type in the writer's registry of types.

        Args:
            type_id (int): The identification number of the type.
            schema (Any): The schema that defines the type.
            name (str, optional): An name to specify, if overriding the type name. Defaults to "".
            scope (Scope | None, optional): The scope in which the type is defined. Defaults to None.

        Returns:
            Type: The registered type.
        """
        if not name:
            name = self.get_display_name(schema)

        if scope is None:
            scope = self.scope.parent

        if scope is None:
            raise ValueError(f"No valid scope was found for registering the type '{name}'.")

        self.type_map[type_id] = retval = CapnpType(schema=schema, name=name, scope=scope)
        return retval

    def is_type_id_known(self, type_id: int) -> bool:
        """Check, whether a type ID was previously registered.

        Args:
            type_id (int): The type ID to check.

        Returns:
            bool: True, if the type ID is known, False otherwise.
        """
        return type_id in self.type_map

    def get_type_by_id(self, type_id: int) -> CapnpType:
        """Look up a type in the type registry, by means of its ID.

        Args:
            type_id (int): The identification number of the type.

        Raises:
            KeyError: If the type ID was not found in the registry.

        Returns:
            Type: The type, if it exists.
        """
        if self.is_type_id_known(type_id):
            return self.type_map[type_id]

        else:
            raise KeyError(f"The type ID '{type_id} was not found in the type registry.'")

    def new_scope(self, name: str, node: Any, scope_heading: str) -> None:
        """Creates a new scope below the scope of the provided node.

        Args:
            name (str): The name of the new scope.
            node (Any): The node whose scope is the parent scope of the new scope.
            scope_heading (str): The line of code that starts this new scope.
        """
        try:
            parent_scope = self.scopes_by_id[node.scopeId]

        except KeyError as e:
            raise NoParentError(f"The scope with name '{name}' has no parent.") from e

        # Add the heading of the scope to the parent scope.
        parent_scope.add_line(scope_heading)

        # Then, make a new scope that is one indent level deeper.
        child_scope = Scope(name=name, id=node.id, parent=parent_scope, return_scope=self.scope)

        self.scope = child_scope
        self.scopes_by_id[node.id] = child_scope

    def return_from_scope(self):
        """Return from the current scope."""
        # Cannot return from the root scope, as it is the highest of all scopes.
        assert not self.scope.is_root

        scope = self.scope
        scope.parent.lines += scope.lines
        self.scope = scope.return_scope

    def get_type_name(self, type_reader: capnp._DynamicStructReader) -> str:
        """Extract the type name from a type reader.

        The output type name is prepended by the scope name, if there is a parent scope.

        Args:
            type_reader (capnp._DynamicStructReader): The type reader to get the type name from.

        Returns:
            str: The extracted type name.
        """
        try:
            return CAPNP_TYPE_TO_PYTHON[type_reader.which()]

        except KeyError:
            pass

        type_reader_type = type_reader.which()

        if type_reader_type == "struct":
            element_type = self.get_type_by_id(type_reader.struct.typeId)
            type_name = element_type.name
            generic_params = []

            for brand_scope in type_reader.struct.brand.scopes:
                brand_scope_type = brand_scope.which()

                if brand_scope_type == "inherit":
                    parent_scope = self.get_type_by_id(brand_scope.scopeId)
                    generic_params.extend(parent_scope.generic_params)

                elif brand_scope_type == "bind":
                    for bind in brand_scope.bind:
                        generic_params.append(self.get_type_name(bind.type))

                else:
                    raise TypeError(f"Unknown brand scope '{brand_scope_type}'.")

            if generic_params:
                type_name += f"[{', '.join(generic_params)}]"

        elif type_reader_type == "enum":
            element_type = self.get_type_by_id(type_reader.enum.typeId)
            type_name = element_type.name

        else:
            raise TypeError(f"Unknown type reader type '{type_reader_type}'.")

        if not element_type.scope.is_root:
            return f"{element_type.scope}.{type_name}"

        else:
            return type_name

    def dumps_pyi(self) -> str:
        """Generates string output for the *.pyi stub file that provides type hinting.

        Returns:
            str: The output string.
        """
        assert self.scope.is_root

        out = []
        out.append(self.docstring)
        out.extend(self.imports)
        out.append("")

        if self.type_vars:
            for name in sorted(self.type_vars):
                out.append(f'{name} = TypeVar("{name}")')
            out.append("")

        out.extend(self.scope.lines)
        return "\n".join(out)

    def dumps_py(self) -> str:
        """Generates string output for the *.py stub file that handles the import of capnproto schemas.

        Returns:
            str: The output string.
        """
        assert self.scope.is_root

        out = []
        out.append(self.docstring)
        out.append("import os")
        out.append("import capnp")
        out.append("capnp.remove_import_hook()")
        out.append("here = os.path.dirname(os.path.abspath(__file__))")

        out.append(f'module_file = os.path.abspath(os.path.join(here, "{self.base_module_name}"))')

        for scope in self.scopes_by_id.values():
            if scope.parent is not None and scope.parent.is_root:
                out.append(f"{scope.name} = capnp.load(module_file).{scope.name}")

        return "\n".join(out)
