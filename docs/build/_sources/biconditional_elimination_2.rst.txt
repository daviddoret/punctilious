biconditional-elimination-2
========================================

.. seealso::
   :doc:`biconditional_elimination_1` | :doc:`biconditional_introduction`

Definition
----------

*biconditional-elimination-2* is the :doc:`inference_rule`:

.. math::

   \left( P \iff Q \right) \vdash \left( Q \implies P \right)

In straightforward language, if P is true if and only if Q is true, it follows that P implies Q.

Quotes
------

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../sample/code/biconditional_elimination_2.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/biconditional_elimination_2_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/biconditional_elimination_2_plaintext.txt
      :language: text
