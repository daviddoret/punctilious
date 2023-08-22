conjunction-introduction
=============================

Definition
----------

*conjunction-introduction* is the well-known and valid :doc:`inference_rule`:

.. math::

    P, Q \vdash \left( P \land Q \right)

Quotes
------

    "The rule of conjunction is a valid argument in types of logic dealing with conjunctions ∧.
    This includes propositional logic and predicate logic, and in particular natural deduction.
    Proof Rule
    If we can conclude both ϕ and ψ, we may infer the compound statement ϕ ∧ ψ."
    - :footcite:p:`proofwiki_2022_ruleconjunction`

Python implementation
--------------------------

Properties
^^^^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: ci, conjunction_introduction

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: ci, conjunction_introduction

Classes
^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: ConjunctionIntroductionDeclaration
    :members:
    :special-members: __init__

.. autoclass:: ConjunctionIntroductionInclusion
    :members:
    :special-members: __init__

Bibliography
------------

.. footbibliography::
