inconsistency-introduction-3
========================================

.. seealso::
   :doc:`inconsistency_introduction_1` | :doc:`inconsistency_introduction_2`

Definition
----------

*inconsistency-introduction-3* is the :doc:`inference_rule`:

.. math::

   \left( P \neq P \right) \vdash Inc\left(\mathcal{T}\right)

In straightforward language, if we prove that an object is not equal to itself, it follows that the theory is inconsistent.

Quotes
----------

   A proof of consistency will have to show, by appealing to contentual considerations which are completely unproblematic, that in the formalism in question it is never possible to derive the formula 𝑎 ≠ 𝑎, or alternatively it is not possible to prove both 𝑎 = 𝑏 and 𝑎 ≠ 𝑏. :cite:p:`mancosu_2021_introductionprooftheorynormalization{p. 5}`


Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../sample/code/inconsistency_introduction_3.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/inconsistency_introduction_3_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/inconsistency_introduction_3_plaintext.txt
      :language: text
