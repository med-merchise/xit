"""Miscellaneous operating system tools."""

from xit.tools import UNSET


def get_env(key: str, default: object = None) -> object:
    """Get a process environment variable.

    The `json.loads`:func: function is used to convert each value.  If any
    error is raised it is ignored and the value remains a string.

    """
    import os
    import json
    from xit.tools.objects import import_object

    UNSET = object()
    if (value := os.environ.get(key, UNSET)) is not UNSET:
        try:
            return json.loads(value)
        except Exception:
            try:
                return import_object(value, silent=False)
            except Exception:
                return value
    else:
        return default


def get_stack_value(
    name: str, *, level: int = 1, default: object = UNSET
) -> object:
    """Return a variable value back in the stack frame level of the caller."""
    import inspect

    frame = inspect.currentframe()
    try:
        deep = level
        while frame and deep > 0:
            frame = frame.f_back
            deep -= 1
        if frame:
            res = frame.f_globals.get(name, default)
            if res is not UNSET:
                return res
            else:
                raise NameError(
                    f"name '{name}' is not defined in stack level {level}"
                )
        else:
            raise RuntimeError(f"no stack frame found at level {level}")
    finally:
        del frame  # avoid memory leaks as recommended in documentation
