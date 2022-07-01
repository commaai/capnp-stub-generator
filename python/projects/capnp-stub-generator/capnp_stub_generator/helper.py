"""Helper functionality that is used in other modules of this package."""


def replace_capnp_suffix(original: str) -> str:
    """If found, replaces the .capnp suffix in a string with _capnp.

    For example, `some_module.capnp` becomes `some_module_capnp`.

    Args:
        original (str): The string to replace the suffix in.

    Returns:
        str: The string with the replaced suffix.
    """
    if original.endswith(".capnp"):
        return original.replace(".capnp", "_capnp")

    else:
        return original
