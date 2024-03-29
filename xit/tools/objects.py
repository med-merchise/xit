"""Several utilities for objects in general."""

from xit.tools import UNSET


def type_name(obj: object) -> str:
    """Return the type name for a given object."""
    try:
        return obj.__name__
    except AttributeError:
        return type(obj).__name__


def short_repr(obj: object, max_len: int = 16) -> str:
    """Return a short string representation of the object.

    Useful in error messages.

    """
    ELLIPSIS = '...'
    if not max_len or max_len < 0:
        max_len = 4
    res = repr(obj)
    if res.startswith('<'):
        res = type_name(obj)
    if len(res) > max_len + len(ELLIPSIS):
        quotes = {'"': '"', "'": "'", '{': '}', '(': ')', '[': ']'}
        if quotes.get(res[0]) == res[-1]:
            head, tail = res[0], res[-1]
            res = res[1:-1]
            max_len -= 2
        else:
            head = tail = ''
        res = head + res[:max_len] + ELLIPSIS + tail
    return res


def is_type(arg: object) -> bool:
    """Return True if `arg` is a type, including those for generic typing."""
    from typing import Any, get_origin

    if isinstance(arg, type):
        return True
    else:
        generic_base = type(Any)
        if generic_base.__base__ is not object:
            generic_base = generic_base.__base__
        return isinstance(arg, generic_base) or get_origin(arg)


def _qstrip(q: str) -> str:
    """Strip a query part (used internally by `get_inner_value`)."""
    q = q.strip()
    return q[1:-1] if len(q) > 2 and q[0] in '"\'' and q[0] == q[-1] else q


def get_inner_value(
    obj: object, query: str, default: object = UNSET
) -> object:
    """Get an object value using a query representing several alternatives.

    A query can have multiple alternatives by using the ``|`` operator as a
    separator.  Each one could be an attribute name, a mapping key, or a
    sequence integer index.

    To see a more elaborated way using path combining a hierarchy of key see
    the function `get_nested_value`:func:.

    """
    from collections.abc import Mapping, Sequence

    WRONG = object()
    parts = query.split('|')
    res = WRONG
    attrs = iter(parts)
    while res is WRONG and (attr := next(attrs, WRONG)) is not WRONG:
        if (aux := getattr(obj, _qstrip(attr), WRONG)) is not WRONG:
            res = aux
    if res is WRONG and isinstance(obj, Mapping):
        keys = iter(parts)
        while res is WRONG and (key := next(keys, WRONG)) is not WRONG:
            if (aux := obj.get(_qstrip(key), WRONG)) is not WRONG:
                res = aux
    if res is WRONG and isinstance(obj, Sequence):
        indexes = iter(parts)
        while res is WRONG and (idx := next(indexes, WRONG)) is not WRONG:
            try:
                res = obj[int(_qstrip(idx))]
            except (ValueError, IndexError):
                pass
    if res is not WRONG:
        return res
    elif default is not UNSET:
        return default
    else:
        raise LookupError(f"Query not found: '{query}'")


def get_nested_value(
    obj: object, path: str, default: object = UNSET
) -> object:
    """Get a nested value.

    This is done by traversing the object's hierarchy by doing operations on
    each part of the path by using the function `get_inner_value`:func:.

    Path parts are split using as separator '.' or '/'.  For example:
    ``'x.y.1'``, or ``'x / y / 1'``.

    Remember you can also do ``eval(path, globals(), vars(obj))`` ;)

    """
    import re

    WRONG = object()
    parts = iter(re.split('[.]|/', path))
    while obj is not WRONG and (key := next(parts, WRONG)) is not WRONG:
        obj = get_inner_value(obj, key, WRONG)
    if obj is not WRONG:
        return obj
    elif default is not UNSET:
        return default
    else:
        raise LookupError(f"Path not found: '{path}'")


def import_object(path: str, silent: bool = False) -> object:
    """Import an object based on a string path.

    .. note::

       This is an adaptation from the ``werkzeug.utilsimport_string``
       function.

    A path can be specified either in dotted notation (``'sys.path'``) or with
    a colon as object delimiter (``'os:environ.USER'``).

    If `silent` is True the return value will be `None` if the import fails.

    """
    import sys
    from importlib import import_module

    try:
        if ':' in path:
            module_name, obj_path = path.split(':')
        else:
            try:
                return import_module(path)
            except ImportError:
                if "." in path:
                    module_name, obj_path = path.rsplit(".", 1)
                else:
                    raise
        module = import_module(module_name)
        return get_nested_value(module, obj_path)
    except Exception as e:
        if silent:
            return None
        else:
            traceback = sys.exc_info()[2]
            raise ImportError(path, e).with_traceback(traceback) from None
