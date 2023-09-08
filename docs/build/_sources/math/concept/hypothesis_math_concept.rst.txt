.. role:: python(code)
    :language: py

hypothesis
========================================

.. seealso::
   :ref:`theory-elaboration-sequence`

Definition
----------

An *hypothesis* is a special statement, that branches out a child :ref:`theory-elaboration-sequence` from a parent :ref:`theory-elaboration-sequence`, and postulates a new :ref:`formula-statement` as true.

Note that an *hypothesis* is part of the theory sequence. It follows that its predecessor statements are contained in the hypothesis, and its successors are not.

In straightforward language, at any point of a theory elaboration, we may pose an hypothesis. That hypothesis is a new "what if" theory that assumes something new to be true.

Quotes
------


Python implementation
----------------------

The simplest way to pose an hypothesis is to call the :python:`pose_hypothesis` method of the :ref:`theory-elaboration-sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # t theory elaboration statements.
   # these are predecessor statements that are contained in the h hypothesis.
   ...
   h = t1.pose_hypothesis(hypothesis_formula=...)
   ...
   # h theory elaboration statements.
   h_theory = h.child_theory # This is the branched out theory of the hypothesis
   h_statement = h.child_statement # This is the formula-statement that constitutes the hypothesis
   ...
   # t theory elaboration statements.
   # these are successor statements that are not contained in the h hypothesis.
   ...

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

   .. literalinclude :: ../../../../sample/code/hypothesis.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/hypothesis_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/hypothesis_plaintext.txt
      :language: text
