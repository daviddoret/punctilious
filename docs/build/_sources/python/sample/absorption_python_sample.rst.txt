.. _absorption_python_sample:

.. role:: python(code)
    :language: py

absorption (python sample)
============================================

.. seealso::
   :ref:`absorption_math_concept` | :ref:`absorption_declaration_python_class` | :ref:`absorption_inclusion_python_class`

This sample python script showcase how to use the :ref:`absorption<absorption_math_concept>` :ref:`inference-rule`.

Usage
----------------------

The simplest way to use the :ref:`absorption<absorption_math_concept>` :ref:`inference-rule` is to access it via the :python:`inference_rules` (abridged :python:`i` ) property of the :ref:`theory-elaboration-sequence`:

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.absorption_1.infer_statement(p_iff_q = ...)

If the :ref:`inference_rule_math_concept` was not yet declared in the :ref:`universe-of-discourse` , it will be automatically declared. If the :ref:`inference_rule_math_concept` was not yet included in the :ref:`theory-elaboration-sequence` , it will be automatically included.

This calls the following method:

.. module:: core
    :noindex:
.. autoclass:: AbsorptionInclusion
    :noindex:
    :members: infer_statement

Source code
----------------------

.. literalinclude :: ../../../../sample/code/absorption.py
  :language: python

Unicode output
-----------------------

.. literalinclude :: ../../../../sample/output/absorption_unicode.txt
  :language: text

Plaintext output
----------------------

   .. literalinclude :: ../../../../sample/output/absorption_plaintext.txt
      :language: text

