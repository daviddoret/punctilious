.. _class_diagram:

.. role:: python(code)
   :language: py

.. tags:: data-model, python, class

Class diagram
========================================================================

.. seealso::
   :ref:`python classes<python_class_index>`

.. graphviz::

   digraph "Punctilious data model" {
      "SymbolicObject" -> "AtheoreticalObject";
      "SymbolicObject" -> "TheoreticalObject";
      "SymbolicObject" -> "UniverseOfDiscourse";
      "TheoreticalObject" -> "Formula";
      "TheoreticalObject" -> "DefinitionDeclaration";
      "TheoreticalObject" -> "InferenceRuleDeclaration";
      "TheoreticalObject" -> "Relation";
      "TheoreticalObject" -> "SimpleObjct";
      "TheoreticalObject" -> "Statement";
      "TheoreticalObject" -> "TheoryDerivation";
      "TheoreticalObject" -> "Variable";
      "Statement" -> "DefinitionInclusion";
      "Statement" -> "FormulaStatement";
      "Statement" -> "Hypothesis";
      "Statement" -> "InferenceRuleInclusion";
      "AtheoreticalObject" -> "NoteInclusion";
      "FormulaStatement" -> "InferredStatement";

   }