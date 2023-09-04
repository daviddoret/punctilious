.. role:: python(code)
    :language: py

conjunction-introduction
=============================

.. seealso::
   :doc:`conjunction_elimination_1` | :doc:`conjunction_elimination_2` | :doc:`inference_rule`

Definition
----------

*conjunction-introduction* is the well-known and valid :doc:`inference_rule`:

.. math::

    (P, Q) \vdash \left( P \land Q \right)

Quotes
------

    "The rule of conjunction is a valid argument in types of logic dealing with conjunctions ∧.
    This includes propositional logic and predicate logic, and in particular natural deduction.
    Proof Rule
    If we can conclude both ϕ and ψ, we may infer the compound statement ϕ ∧ ψ."
    - :footcite:p:`proofwiki_2022_ruleconjunction`


Python implementation
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :doc:`theory_elaboration_sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.conjunction_introduction.infer_statement(p = ..., q = ...)

If the :doc:`inference_rule` was not yet declared in the :doc:`universe_of_discourse` , it will be automatically declared. If the :doc:`inference_rule` was not yet included in the :doc:`theory_elaboration_sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: ConjunctionIntroductionInclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../sample/code/conjunction_introduction.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/conjunction_introduction_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/conjunction_introduction_plaintext.txt
      :language: text
