"""File system utilities."""


def trim(name: str, n: int = 1) -> str:
    """Trims the last `n` components of the path-name."""
    import os

    res = os.path.expanduser(os.path.normpath(name))
    while n > 0:
        res = os.path.dirname(res)
        n -= 1
    return res
