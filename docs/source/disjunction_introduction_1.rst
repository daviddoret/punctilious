disjunction-introduction-1
===============================

Definition
----------

*disjunction-introduction-left* is the well-known and valid :doc:`inference_rule`:

.. math::

    P \vdash \left( Q \lor P \right)

Quotes
------

    "Addition (or disjunction introduction, or or introduction) is the rule of inference that allows one to infer a disjunction from either of the disjuncts."
    - :footcite:p:`cook_2009_dictionaryphilosophicallogic`, p8

Python implementation
--------------------------

Properties
^^^^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: disjunction_introduction_left

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: disjunction_introduction_left

Classes
^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: DisjunctionIntroductionLeftDeclaration
    :members:
    :special-members: __init__

.. autoclass:: DisjunctionIntroductionLeftInclusion
    :members:
    :special-members: __init__

Bibliography
------------

.. footbibliography::
