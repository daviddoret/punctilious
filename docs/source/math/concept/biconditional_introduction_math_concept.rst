.. _biconditional_introduction_math_concept:
.. _biconditional-introduction:

.. role:: python(code)
    :language: py

biconditional-introduction
========================================

.. seealso::
   :ref:`biconditional-elimination-1` | :ref:`biconditional-elimination-2` | :ref:`inference-rule`

Definition
----------

*biconditional-introduction* is the :ref:`inference-rule`:

.. math::

   \left( \left( P \implies Q \right), \left( Q \implies P \right) \right) \vdash \left( Q \iff P \right)

Where:

* :math:`P \implies Q` is a :ref:`formula_statement`
* :math:`Q \implies P` is a :ref:`formula_statement`
* :math:`P` is a propositional :ref:`formula`
* :math:`Q` is a propositional :ref:`formula`

In straightforward language, if P implies Q and Q implies P, it follows that P if and only if Q.

Quotes
------


Python implementation
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :ref:`theory-elaboration-sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.biconditional_introduction.infer_statement(p_iff_q = ...)

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: BiconditionalIntroductionInclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/biconditional_introduction.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/biconditional_introduction_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/biconditional_introduction_plaintext.txt
      :language: text
