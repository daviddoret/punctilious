.. role:: python(code)
    :language: py

double-negation-introduction
=============================

.. seealso::
   :ref:`double_negation_elimination` | :ref:`inference_rule_math_concept`

Definition
----------

*double-negation-introduction* is the well-known and valid :ref:`inference_rule_math_concept`:

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
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :ref:`theory-elaboration-sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.double_negation_introduction.infer_statement(p = ...)

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: DoubleNegationIntroductionInclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/double_negation_introduction.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/double_negation_introduction_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/double_negation_introduction_plaintext.txt
      :language: text
