.. role:: python(code)
    :language: py

disjunction-introduction-1
===============================

.. seealso::
   :doc:`disjunction_introduction_2` | :doc:`inference_rule`

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
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :doc:`theory_elaboration_sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   p = ... # some inferred-statement
   q = ... # any formula
   ...
   t.i.disjunction_introduction_1.infer_statement(p = ..., q = ...)

If the :doc:`inference_rule` was not yet declared in the :doc:`universe_of_discourse` , it will be automatically declared. If the :doc:`inference_rule` was not yet included in the :doc:`theory_elaboration_sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: DisjunctionIntroduction1Inclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../sample/code/disjunction_introduction_1.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/disjunction_introduction_1_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/disjunction_introduction_1_plaintext.txt
      :language: text
