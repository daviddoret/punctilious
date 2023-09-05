.. role:: python(code)
    :language: py

biconditional-elimination-1
========================================

.. seealso::
   :doc:`biconditional_elimination_2` | :doc:`biconditional_introduction` | :ref:`inference_rule_math_concept`

Definition
----------

*biconditional-elimination-1* is the :ref:`inference_rule_math_concept`:

.. math::

   \left( P \iff Q \right) \vdash \left( P \implies Q \right)

Where:

* :math:`P \iff Q` is a :doc:`formula_statement`
* :math:`P` is a propositional :doc:`formula`
* :math:`Q` is a propositional :doc:`formula`

In straightforward language, if P is true if and only if Q is true, it follows that P implies Q.

Quotes
------

Python implementation
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :ref:`theory_elaboration_sequence_math_concept`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.biconditional_elimination_1.infer_statement(p_iff_q = ...)

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe_of_discourse_math_concept` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory_elaboration_sequence_math_concept` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: BiconditionalElimination1Inclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/biconditional_elimination_1.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/biconditional_elimination_1_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/biconditional_elimination_1_plaintext.txt
      :language: text
