.. role:: python(code)
    :language: py

disjunction-introduction-1
===============================

.. seealso::
   :ref:`disjunction_introduction_2` | :ref:`inference_rule_math_concept`

Definition
----------

*disjunction-introduction-left* is the well-known and valid :ref:`inference_rule_math_concept`:

.. math::

    P \vdash \left( Q \lor P \right)

Quotes
------

    "Addition (or disjunction introduction, or or introduction) is the rule of inference that allows one to infer a disjunction from either of the disjuncts."
    - :footcite:p:`cook_2009_dictionaryphilosophicallogic`, p8


Python implementation
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :ref:`theory-elaboration-sequence`:

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

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

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

   .. literalinclude :: ../../../../sample/code/disjunction_introduction_1.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/disjunction_introduction_1_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/disjunction_introduction_1_plaintext.txt
      :language: text
