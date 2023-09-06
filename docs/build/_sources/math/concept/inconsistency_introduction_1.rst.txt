.. role:: python(code)
    :language: py

inconsistency-introduction-1
========================================

.. seealso::
   :ref:`inconsistency_introduction_2` | :ref:`inconsistency_introduction_3`

Definition
----------

*inconsistency-introduction-1* is the :ref:`inference_rule_math_concept`:

.. math::

   \left( P, \neg \left(P\right) \right) \vdash Inc\left(\mathcal{T}\right)

In straightforward language, if we prove a proposition and its negation, it follows that the theory is inconsistent.

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
   t.i.inconsistency_introduction_1.infer_statement(p = ...)

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: InconsistencyIntroduction1Inclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/inconsistency_introduction_1.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/inconsistency_introduction_1_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/inconsistency_introduction_1_plaintext.txt
      :language: text
