absorption
==========

Definition
----------

*absorption* is the well-known and valid :doc:`inference_rule` in propositional-logic:

.. math::

    \left(P \implies Q\right) \vdash \left(P \implies P \land Q\right)

Python implementation
---------------------

AbsorptionDeclaration
^^^^^^^^^^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: AbsorptionDeclaration
    :members:
    :special-members: __init__

AbsorptionInclusion
^^^^^^^^^^^^^^^^^^^

.. autoclass:: AbsorptionInclusion
    :members:
    :special-members: __init__

Bibliography
------------

* https://en.wikipedia.org/wiki/Absorption_(logic)
