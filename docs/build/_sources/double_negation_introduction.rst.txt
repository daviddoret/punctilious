double-negation-introduction
=============================

Definition
----------

*double-negation-introduction* is the well-known and valid :doc:`inference_rule`:

.. math::

    P \vdash \lnot \left( \lnot \left( P \right) \right)

Quotes
------

    "The rule of double negation introduction is a valid argument in types of logic dealing with negation ¬.
    This includes propositional logic and predicate logic, and in particular natural deduction.
    As a proof rule it is expressed in the form:
    If we can conclude ϕ, then we may infer ¬¬ϕ."
    - :footcite:p:`proofwiki_2022_doublenegation`

Python implementation
--------------------------

Properties
^^^^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: dni, double_negation_introduction

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: dni, double_negation_introduction

Classes
^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: DoubleNegationIntroductionDeclaration
    :members:
    :special-members: __init__

.. autoclass:: DoubleNegationIntroductionInclusion
    :members:
    :special-members: __init__

Bibliography
------------

.. footbibliography::
