"""Miscellaneous operating system tools."""


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
