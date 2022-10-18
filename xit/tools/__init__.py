"""Collection of very simple tools not tied to any specific framework."""


class Unset:
    """Class for a false marker value.

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


def named_lambda(**kwargs: callable) -> callable:
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
    try:
        return getattr(obj, name)
    except AttributeError:
        setattr(obj, name, default)
        return default


def current_process_contains(arg: str) -> bool:
    """Return True if `arg` is in the list of current parent processes."""
    import psutil

    arg = arg.lower()
    cp = psutil.Process()
    return next(
        (True for p in cp.parents() if arg in p.name().lower()),
        False,
    )


def get_line(text: str, /, index: int = 0, strip_chars: str = None) -> str:
    """Get line at index in a text."""
    if text:
        items = text.split('\n')
        if 0 <= index < len(items):
            res = items[index]
            return res.strip(strip_chars) if strip_chars else res
        else:
            return ''
    else:
        return ''


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
