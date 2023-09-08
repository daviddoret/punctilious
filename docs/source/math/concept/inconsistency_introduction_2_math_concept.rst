.. _inconsistency_introduction_2_math_concept:
.. _inconsistency-introduction-2:

.. role:: python(code)
    :language: py

inconsistency-introduction-2
========================================

.. seealso::
   :ref:`inconsistency-introduction-1` | :ref:`inconsistency-introduction-3`

Definition
----------

*inconsistency-introduction-2* is the :ref:`inference-rule`:

.. math::

   \left(\left(x = y\right), \left(x \neq y\right)\right) \vdash Inc\left(\mathcal{T}\right)

In straightforward language, if we prove both the equality and inequality of two terms, it follows that the theory is inconsistent.

Quotes
----------

   A proof of consistency will have to show, by appealing to contentual considerations which are completely unproblematic, that in the formalism in question it is never possible to derive the formula 𝑎 ≠ 𝑎, or alternatively it is not possible to prove both 𝑎 = 𝑏 and 𝑎 ≠ 𝑏. :cite:p:`mancosu_2021_introductionprooftheorynormalization{p. 5}`

Python implementation
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :ref:`theory-elaboration-sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.inconsistency_introduction_2.infer_statement(p = ...)

If the :ref:`inference-rule` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference-rule` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: InconsistencyIntroduction2Inclusion
    :noindex:
    :members: infer_statement


Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/inconsistency_introduction_2.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/inconsistency_introduction_2_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/inconsistency_introduction_2_plaintext.txt
      :language: text
