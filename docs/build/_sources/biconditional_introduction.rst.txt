biconditional-introduction
========================================

.. seealso::
   :doc:`biconditional_elimination_1` | :doc:`biconditional_elimination_2`

Definition
----------

*biconditional-introduction* is the :doc:`inference_rule`:

.. math::

   \left( \left( P \implies Q \right), \left( Q \implies P \right) \right) \vdash \left( Q \iff P \right)

In straightforward language, if P implies Q and Q implies P, it follows that P if and only if Q.

Quotes
------

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../sample/code/biconditional_introduction.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/biconditional_introduction_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/biconditional_introduction_plaintext.txt
      :language: text
