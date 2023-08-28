biconditional-elimination-left
========================================

Definition
----------

*biconditional-elimination-left* is the :doc:`inference_rule`:

.. math::

   \left( P \iff Q \right) \vdash \left( P \implies Q \right)

In straightforward language, if P is true if and only if Q is true, it follows that P implies Q.

Quotes
------

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../sample/code/biconditional_elimination_left.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/biconditional_elimination_left_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/biconditional_elimination_left_plaintext.txt
      :language: text
