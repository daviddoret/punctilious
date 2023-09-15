.. _absorption_python_sample:

.. role:: python(code)
    :language: py

.. tags:: absorption, python, sample

absorption (python sample)
============================================

.. seealso::
   :ref:`math concept<absorption_math_concept>` | :ref:`python declaration class<absorption_declaration_python_class>` | :ref:`python inclusion class<absorption_inclusion_python_class>`

This sample python script showcase how to use the :ref:`absorption<absorption_math_concept>` :ref:`inference-rule`.

Usage
----------------------

The simplest way to use the :ref:`absorption<absorption_math_concept>` :ref:`inference-rule` is to access it via the :python:`i` (unabridged :python:`inference_rules` ) property of the :ref:`theory-elaboration-sequence` :

.. code-block:: python

   u = pu.create_universe()
   t = u.t()
   ...
   # some theory elaboration code
   ...
   t.i.absorption.infer_statement(p_iff_q = ...)

Sample code
----------------------

.. literalinclude :: ../../../../src/sample/sample_absorption.py
  :language: python

Code output
-----------------------

.. tabs::

   .. tab:: Unicode

      .. literalinclude :: ../../../../data/sample_absorption_unicode.txt
         :language: text

   .. tab:: Plaintext

      .. literalinclude :: ../../../../data/sample_absorption_Plaintext.txt
         :language: text

   .. tab:: LaTeX

      Will be provided in a future version.

   .. tab:: HTML

      Will be provided in a future version.