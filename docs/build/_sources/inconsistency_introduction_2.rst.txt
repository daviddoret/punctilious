inconsistency-introduction-2
========================================

Definition
----------

*inconsistency-introduction-2* is the :doc:`inference_rule`:

.. math::

   \left(\left(x = y\right), \left(x \neq y\right)\right) \vdash Inc\left(\mathcal{T}\right)

In straightforward language, if we prove both the equality and inequality of two terms, it follows that the theory is inconsistent.

Quotes
----------

   A proof of consistency will have to show, by appealing to contentual considerations which are completely unproblematic, that in the formalism in question it is never possible to derive the formula 𝑎 ≠ 𝑎, or alternatively it is not possible to prove both 𝑎 = 𝑏 and 𝑎 ≠ 𝑏. :cite:p:`mancosu_2021_introductionprooftheorynormalization{p. 5}`


Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../sample/code/inconsistency_introduction_2.py
      :language: python
      :linenos:

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/inconsistency_introduction_2_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../sample/output/inconsistency_introduction_2_plaintext.txt
      :language: text
