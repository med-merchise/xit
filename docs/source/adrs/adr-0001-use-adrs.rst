.. _adr-0001:

ADR 1: Use Architecture Decision Records (ADRs)
===============================================


Status
------

Accepted


Context
-------

We need to record the architectural decisions made on this project.


Decision
--------

We will use ADRs, as `described by Michael Nygard <nygard_>`__.

.. _nygard: http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions


Consequences
------------

The ADRs in this project are in the architectural level of Foundation and
Common Systems.  Other projects may simply reference this one to "inherit"
them from here.

We could some additional document types (like `RFCs <adr-0002>`:ref:) to
complement this main type of documents.

See Michael Nygard's article, linked above.  For a lightweight ADR tool-set,
see Nat Pryce's adr-tools_.

For more information see a `good repository by Joel Parker Henderson <jph_>`__
about this subject.

.. _adr-tools: https://github.com/npryce/adr-tools
.. _jph: https://github.com/joelparkerhenderson/architecture-decision-record
