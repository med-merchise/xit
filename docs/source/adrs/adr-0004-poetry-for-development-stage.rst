ADR 4: Use Poetry for Development Stage
=======================================


Status
------

Accepted


Context
-------

We need a way to develop and evolve several projects at the same time.


Decision
--------

We will use poetry_ for:

- Dependency Management.
- Packaging.
- Publish (when open or free-software license is used).
- Execute local tests.

.. _poetry: https://python-poetry.org


Consequences
------------

Make sure `poetry is installed <poetry-install_>`__, they say the preferred
option is::

  curl -sSL https://install.python-poetry.org | python -

See how to `enable tab-completion for poetry <poetry-tc_>`__, we use Linux
with ``bash`` on the user home location::

  COMPLETIONS_PATH=$HOME/.local/share/bash-completion/completions
  poetry completions bash > $COMPLETIONS_PATH/poetry

.. _poetry-install: https://python-poetry.org/docs/#installation
.. _poetry-tc: https://python-poetry.org/docs/#enable-tab-completion-for-bash-fish-or-zsh

I prefer to create virtual-enviroments inside the project's root directory,
configure it using::

  poetry config virtualenvs.in-project true

This option can be configured also local per project::

  cd <PROJECT-PATH>
  poetry config virtualenvs.in-project true --local

To make sure all dependencies are installed in a consistent way, execute the
following commands::

  poetry lock --no-update
  poetry install --sync
  poetry update
