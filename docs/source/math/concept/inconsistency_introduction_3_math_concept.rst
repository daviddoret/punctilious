.. role:: python(code)
    :language: py

inconsistency-introduction-3
========================================

.. seealso::
   :ref:`inconsistency_introduction_1` | :ref:`inconsistency_introduction_2`

Definition
----------

*inconsistency-introduction-3* is the :ref:`inference-rule`:

.. math::

   \left( P \neq P \right) \vdash Inc\left(\mathcal{T}\right)

In straightforward language, if we prove that an object is not equal to itself, it follows that the theory is inconsistent.

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
   t.i.inconsistency_introduction_3.infer_statement(p = ...)

If the :ref:`inference-rule` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference-rule` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: InconsistencyIntroduction3Inclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/inconsistency_introduction_3.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/inconsistency_introduction_3_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/inconsistency_introduction_3_plaintext.txt
      :language: text
