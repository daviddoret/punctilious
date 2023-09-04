.. role:: python(code)
    :language: py

conjunction-elimination-2
========================================

.. seealso::
   :doc:`conjunction_elimination_1` | :doc:`conjunction_introduction` | :doc:`inference_rule`

Definition
----------

*conjunction-elimination-2* is the :doc:`inference_rule`:

.. math::

   \left( P \land Q \right) \vdash Q

In straightforward language, if "P and Q" is true, it follows that Q is true.

Quotes
------


Python implementation
----------------------

The simplest way to use this inference-rule is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :doc:`theory_elaboration_sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.conjunction_elimination_2.infer_statement(p_and_q = ...)

If the :doc:`inference_rule` was not yet declared in the :doc:`universe_of_discourse` , it will be automatically declared. If the :doc:`inference_rule` was not yet included in the :doc:`theory_elaboration_sequence` , it will be automatically included.

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

   .. literalinclude :: ../../../sample/code/conjunction_elimination_2.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/conjunction_elimination_2_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/conjunction_elimination_2_plaintext.txt
      :language: text
