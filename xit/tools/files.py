"""File system utilities."""

import os


def _isdir(name: str) -> bool:
    """Return true if the path-name refers to a directory.

    Could be because it is an existing directory or a path ending with
    `os.sep` character.

    """
    return os.path.isdir(name) or name.endswith(os.sep)


def trim(name: str, n: int = 1) -> str:
    """Trims the last `n` components of the path-name."""
    res = os.path.expanduser(os.path.normpath(name))
    while n > 0:
        res = os.path.dirname(res)
        n -= 1
    return res


def expand_filenames(*names: str, base_dir: str = None) -> str:
    """Join several file names with the base directory component."""
    if base_dir is not None:
        if not _isdir(base_dir):
            base_dir = trim(base_dir)
    elif len(names) and _isdir(names[0]):
        base_dir = names[0]
        names = names[1:]
    else:
        base_dir = os.path.abspath(os.curdir)
    if not names:
        names = ('',)
    res = os.path.join(base_dir, *names)
    return os.path.join(res, '') if os.path.isdir(res) else res
