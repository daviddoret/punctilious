.. _conjunction_elimination_2_math_concept:
.. _conjunction-elimination-2:

.. role:: python(code)
    :language: py

conjunction-elimination-2
========================================

.. seealso::
   :ref:`conjunction-elimination-1` | :ref:`conjunction-introduction` | :ref:`inference-rule`

Definition
----------

*conjunction-elimination-2* is the :ref:`inference-rule`:

.. math::

   \left( P \land Q \right) \vdash Q

In straightforward language, if "P and Q" is true, it follows that Q is true.

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
   t.i.conjunction_elimination_2.infer_statement(p_and_q = ...)

If the :ref:`inference-rule` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference-rule` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: ConjunctionElimination2Inclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../src/sample/sample_conjunction_elimination_2.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../data/sample_conjunction_elimination_2_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../data/sample_conjunction_elimination_2_plaintext.txt
      :language: text
