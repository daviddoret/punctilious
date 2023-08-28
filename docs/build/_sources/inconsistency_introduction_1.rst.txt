inconsistency-introduction-1
========================================

.. seealso::
   :doc:`inconsistency_introduction_2` | :doc:`inconsistency_introduction_3`

Definition
----------

*inconsistency-introduction-1* is the :doc:`inference_rule`:

.. math::

   \left( P, \neg \left(P\right) \right) \vdash Inc\left(\mathcal{T}\right)

In straightforward language, if we prove a proposition and its negation, it follows that the theory is inconsistent.

Quotes
------

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../sample/code/inconsistency_introduction_1.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/inconsistency_introduction_1_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/inconsistency_introduction_1_plaintext.txt
      :language: text
