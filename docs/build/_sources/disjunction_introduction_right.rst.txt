disjunction-introduction-right
===============================

Definition
----------

*disjunction-introduction-right* is the well-known and valid :doc:`inference_rule`:

.. math::

    P \vdash \left( P \lor Q \right)

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
    :members: disjunction_introduction_right

.. module:: core
    :noindex:
.. autoclass:: InferenceRuleDeclarationDict
    :noindex:
    :members: disjunction_introduction_right

Classes
^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: DisjunctionIntroductionRightDeclaration
    :members:
    :special-members: __init__

.. autoclass:: DisjunctionIntroductionRightInclusion
    :members:
    :special-members: __init__

Bibliography
------------

.. footbibliography::
