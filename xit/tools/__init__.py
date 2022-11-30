"""Collection of very simple tools not tied to any specific framework."""

from typing import Callable, Sequence


class Unset:
    """Class for a false marker singleton value.

    Useful as a replacement when `None` could be one of the expected valid
    values.

    """

    _singleton: 'Unset' = None

    def __new__(cls):  # noqa
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __bool__(self) -> bool:  # noqa
        return False


UNSET: Unset = Unset()


def named_lambda(**kwargs: Callable) -> Callable:
    """Return a named lambda function.

    Only one value must be provider in the `kwargs` parameters.  For example::

        >>> sum = named_lambda(sum=lambda df: df.sum(axis=1))

    """
    count = len(kwargs)
    if count == 1:
        name, fun = next(iter(kwargs.items()))
        fun.__name__ = fun.__qualname__ = name
        return fun
    else:
        raise ValueError(
            f"Invalid number of arguments, one expented, {count} given"
        )


def sda(obj: object, name: str, default: object = None) -> object:
    """Set default attribute value.

    Inserts the attribute with a value of 'default' if the object does not
    already have an attribute with the given 'name'.

    Return the value for 'name' if already present, else 'default'.

    """
    UNSET = object()
    res = getattr(obj, name, UNSET)
    if res is UNSET:
        setattr(obj, name, default)
        res = default
    return default


def safe_call(fn: Callable) -> object:
    """Call function in a safe context, return None if any error is raised."""
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwds):
        try:
            return fn(*args, **kwds)
        except Exception:
            return None

    return inner


def current_process_contains(arg: str) -> bool:
    """Return True if `arg` is in the list of current parent processes."""
    import psutil

    arg = arg.lower()
    cp = psutil.Process()
    return next(
        (True for p in cp.parents() if arg in p.name().lower()),
        False,
    )


def get_paragraphs(text: str) -> list[str]:
    """Get non-empty paragraphs in a text."""
    res = []
    for part in text.split('\n\n'):
        aux = ' '.join(line.rstrip() for line in part.rstrip().split('\n'))
        if aux:
            res.append(aux)
    return res


def common_prefix(*items: Sequence) -> int:
    """Determine the common prefix from a set of sequences.

    Returns the count of common elements in all sequences, for example::

      >>> common_prefix("Hello World!", "Hello world!")
      6

      >>> common_prefix('h.e.l.l.o'.split('.'), 'help')
      3

    """
    count = len(items)
    if count > 0:
        min_len = min(map(len, items))
        base, items = items[0], items[1:]
        idx, ok = 0, True
        while ok and idx < min_len:
            if all(base[idx] == item[idx] for item in items):
                idx += 1
            else:
                ok = False
        return idx
    else:
        raise TypeError(
            "common_prefix() missing at least 1 required positional argument"
        )


class slicer:
    """A simple syntax constructor for `slice` instances.

    For example::

      >>> slicer[1:10:2] == slice(1, 10, 2)
      >>> slicer[10] == 10

    """

    def __new__(cls, *args: object) -> slice:
        """Create a slice object (no need to use this)."""
        return slice(*args)

    def __class_getitem__(cls, index: object) -> object:
        """Create the slice the correct way."""
        return index
