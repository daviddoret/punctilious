variable-substitution
=====================

Definition
----------

*variable-substitution* is the well-known and valid :ref:`inference-rule`:

.. math::

    \left( P, \Phi \right)  \vdash Q'

Where:
* P is any valid formula-statement that contains n variables,
* Phi is a sequence of n well-formed formulae,
* Q is a modified P formula-statement where variables in P have been replaced by the corresponding formulae in Phi

Python implementation
---------------------

VariableSubstitutionDeclaration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: VariableSubstitutionDeclaration
    :members:
    :special-members: __init__

VariableSubstitutionInclusion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: VariableSubstitutionInclusion
    :members:
    :special-members: __init__

Bibliography
------------

* ...
