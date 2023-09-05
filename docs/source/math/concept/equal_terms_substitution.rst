.. role:: python(code)
    :language: py

equal-terms-substitution
=============================

.. seealso::
   :doc:`equality_commutativity` | :ref:`inference_rule_math_concept`

Definition
----------

*equal-terms-substitution* is the well-known and valid :ref:`inference_rule_math_concept`:

.. math::

    \left( P, x = y \right) \vdash Q

Where:

* :math:`P` is a :doc:`formula_statement`
* :math:`x = y` is a :doc:`formula_statement` of the form :math:`x = y`
* :math:`Q` is a :doc:`formula_statement` identical to :math:`P` except that every occurrences of :math:`x` in :math:`P` are substituted with :math:`y`

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
   t.i.equal-terms_substitution.infer_statement(p = ...)

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe_of_discourse_math_concept` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory_elaboration_sequence_math_concept` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: EqualTermsSubstitutionInclusion
    :noindex:
    :members: infer_statement

Python sample usage
----------------------

.. admonition:: Source code
  :class: tip, dropdown

   .. literalinclude :: ../../../../sample/code/equal_terms_substitution.py
      :language: python

.. admonition:: Unicode output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/equal_terms_substitution_unicode.txt
      :language: text

.. admonition:: Plaintext output
   :class: note, dropdown

   .. literalinclude :: ../../../../sample/output/equal_terms_substitution_plaintext.txt
      :language: text
