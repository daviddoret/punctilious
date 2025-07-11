.. _destructive_dilemma_python_sample:

..
   rst file generated by generate_docs_inference_rules.py.

.. role:: python(code)
    :language: py

destructive-dilemma (python sample)
============================================

.. tags:: destructive-dilemma, python, sample

.. seealso::
   :ref:`math concept<destructive_dilemma_math_inference_rule>` | :ref:`python declaration class<destructive_dilemma_declaration_python_class>` | :ref:`python inclusion class<destructive_dilemma_inclusion_python_class>`

This page shows how to infer new statements in a theory-derivation by applying the :ref:`destructive-dilemma<destructive_dilemma_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>`.

Usage
----------------------

Call the :python:`infer_statement` method from the inference-rule inclusion class listed in the :python:`i` (unabridged :python:`inference_rules` ) property of the :ref:`theory-derivation<theory_derivation_math_concept>` :

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.destructive_dilemma.infer_statement(...)

Sample code
----------------------

.. literalinclude :: ../../../../src/sample/sample_destructive_dilemma.py
:language: python

Code output
-----------------------

.. tabs::

   .. tab:: Unicode

      .. literalinclude :: ../../../../data/sample_destructive_dilemma_unicode.txt
:language: text

   .. tab:: Plaintext

      .. literalinclude :: ../../../../data/sample_destructive_dilemma_plaintext.txt
:language: text

   .. tab:: LaTeX

      Will be provided in a future version.

   .. tab:: HTML

      Will be provided in a future version.