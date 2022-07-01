"""Types definitions that are common in capnproto schemas."""
from types import ModuleType
from typing import Dict, Tuple

CAPNP_TYPE_TO_PYTHON = {
    "void": "None",
    "bool": "bool",
    "int8": "int",
    "int16": "int",
    "int32": "int",
    "int64": "int",
    "uint8": "int",
    "uint16": "int",
    "uint32": "int",
    "uint64": "int",
    "float32": "float",
    "float64": "float",
    "text": "str",
    "data": "bytes",
}

class CapnpFieldType:
    """Types of capnproto fields."""

    GROUP = "group"
    SLOT = "slot"


class CapnpSlotType:
    """Types of capnproto slots.

    If CapnpFieldType is 'slot', this defines the type of that slot.
    """

    ANY_POINTER = "anyPointer"
    STRUCT = "struct"
    ENUM = "enum"
    LIST = "list"


class CapnpElementType:
    """Types of capnproto elements."""

    ENUM = "enum"
    STRUCT = "struct"
    CONST = "const"


ModuleRegistryType = Dict[int, Tuple[str, ModuleType]]
