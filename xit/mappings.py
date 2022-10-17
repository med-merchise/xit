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


def pop_items(source: dict, *keys) -> dict:
    """Pop a collection of keys from a source dictionary."""
    return {key: source.pop(key, None) for key in keys if key in source}


def asdict(obj: object) -> dict[str, object]:
    """Return a new dictionary mapping from a given object.

    The function applies recursively to field values that are
    dataclass instances.

    """
    from collections.abc import Mapping
    import dataclasses as dc

    if not isinstance(obj, type):
        if callable(getattr(obj, 'asdict', None)):
            return obj.asdict()
        elif dc.is_dataclass(obj):
            return dc.asdict(obj)
        elif callable(getattr(obj, 'dict', None)):  # pydantic
            return obj.dict()
        elif isinstance(obj, Mapping):
            return dict(obj)
        else:
            tname = type(obj).__name__
            raise TypeError(
                f"asdict() should not be called on '{tname}' instances."
            )
    else:
        raise TypeError(
            f"asdict() should not be called on '{obj.__name__}' type."
        )
