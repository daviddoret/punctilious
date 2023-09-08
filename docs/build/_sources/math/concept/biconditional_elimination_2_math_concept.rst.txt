.. _biconditional_elimination_2_math_concept:
.. _biconditional-elimination-2:

.. role:: python(code)
    :language: py

biconditional-elimination-2
========================================

.. seealso::
   :ref:`biconditional-elimination-1` | :ref:`biconditional-introduction` | :ref:`inference-rule`

Definition
----------

*biconditional-elimination-2* is the :ref:`inference-rule`:

.. math::

   \left( P \iff Q \right) \vdash \left( Q \implies P \right)

Where:

* :math:`P \iff Q` is a :ref:`formula-statement`
* :math:`P` is a propositional :ref:`formula`
* :math:`Q` is a propositional :ref:`formula`

In straightforward language, if P is true if and only if Q is true, it follows that P implies Q.

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
   t.i.biconditional_elimination_2.infer_statement(p_iff_q = ...)

If the :ref:`inference-rule` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference-rule` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: BiconditionalElimination2Inclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/biconditional_elimination_2.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/biconditional_elimination_2_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/biconditional_elimination_2_plaintext.txt
      :language: text
