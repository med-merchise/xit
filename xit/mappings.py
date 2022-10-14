"""General mappings tools."""

from collections.abc import Mapping


def flatten_dict(source: Mapping, sep: str = '.', prefix: str = '') -> dict:
    """Get a flatten dictionary."""
    res = {}
    for key, value in source.items():
        inner_prefix = prefix + sep + key if prefix else key
        if value and isinstance(value, Mapping):
            res.update(flatten_dict(value, sep, inner_prefix))
        else:
            res[inner_prefix] = value
    return res
