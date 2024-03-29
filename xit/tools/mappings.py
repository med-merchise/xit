"""General mappings tools."""

from collections.abc import Mapping
from typing import Callable, Type


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


def unflatten_dict(source: Mapping, sep: str = '.') -> dict:
    """Get a unflatten dictionary."""
    res = {}
    for key, value in source.items():
        if sep in key:
            pivot = res
            *parts, tail = key.split(sep)
            for part in parts:
                pivot = pivot.setdefault(part, {})
            pivot[tail] = value
        else:
            res[key] = value
    return res


def pop_items(source: dict, *keys, **defaults) -> dict:
    """Get a dictionary by popping 'keys' and 'defaults' from 'source'."""
    res = {key: source.pop(key) for key in keys if key in source}
    for key, value in defaults.items():
        res.setdefault(key, source.pop(key, value))
    return res


def asdict(
    obj: object,
    filter_key: str | Type | tuple | Callable[[object], bool] | None = '_',
) -> dict[str, object]:
    """Return a mapping from a given object.

    :param filter_key: could be a prefix string (keys starting with that
           prefix won't be included); a type or tuple of types, key is checked
           to be an instance of any of those types; a callable to check which
           keys are ok to be included; or None to include all keys.

    """
    # TODO: support `attrs` library?
    import dataclasses as dc
    from xit.tools import safe_call

    match filter_key:
        case class_or_tuple if isinstance(class_or_tuple, (type, tuple)):
            ok = lambda key: isinstance(key, class_or_tuple)  # noqa: E731
        case str(prefix):
            ok = lambda key: (  # noqa: E731
                isinstance(key, str) and not key.startswith(prefix)
            )
        case check if callable(check):
            ok = safe_call(check)
        case None | False:
            ok = lambda key: True  # noqa: E731
        case _:
            raise TypeError(filter_key)
    if not isinstance(obj, type):
        try:
            if callable(getattr(obj, 'asdict', None)):
                res = obj.asdict()
            elif dc.is_dataclass(obj):
                res = dc.asdict(obj)
            elif callable(getattr(obj, 'dict', None)):  # pydantic
                res = obj.dict()
            else:
                res = dict(obj)
            res = res.items()
        except Exception:
            res = None
    else:
        res = None
    if res is None:
        try:
            res = obj.__dict__.items()
        except AttributeError:
            res = ((key, getattr(obj, key)) for key in dir(obj))
    return {key: value for key, value in res if ok(key)}
