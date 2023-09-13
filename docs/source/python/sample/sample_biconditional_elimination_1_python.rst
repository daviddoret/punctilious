.. _biconditional_elimination_1_python_sample:

.. role:: python(code)
    :language: py

.. tags:: biconditional-elimination-1, python, sample

biconditional-elimination-1 (python sample)
============================================

.. seealso::
   :ref:`math concept<biconditional_elimination_1_math_concept>` | :ref:`python declaration class<biconditional_elimination_1_declaration_python_class>` | :ref:`python inclusion class<biconditional_elimination_1_inclusion_python_class>`

This sample python script showcase how to use the :ref:`biconditional-elimination-1<biconditional_elimination_1_math_concept>` :ref:`inference-rule`.

Usage
----------------------

The simplest way to use the :ref:`biconditional-elimination-1<biconditional_elimination_1_math_concept>` :ref:`inference-rule` is to access it via the :python:`i` (unabridged :python:`inference_rules` ) property of the :ref:`theory-elaboration-sequence` :

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.biconditional_elimination_1.infer_statement(p_iff_q = ...)

Sample code
----------------------

.. literalinclude :: ../../../../src/sample/sample_biconditional_elimination_1.py
  :language: python

Code output
-----------------------

.. tabs::

   .. tab:: Unicode

      .. literalinclude :: ../../../../data/sample_biconditional_elimination_1_unicode.txt
         :language: text

   .. tab:: Plaintext

      .. literalinclude :: ../../../../data/sample_biconditional_elimination_1_Plaintext.txt
         :language: text

   .. tab:: LaTeX

      Will be provided in a future version.

   .. tab:: HTML

      Will be provided in a future version.