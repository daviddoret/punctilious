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
      rankdir = LR;
      node [shape=box];
      fontname="Arial";
      fontsize="20pt";

      Formula [style=filled, fillcolor="#FEFE62"];
      AxiomDeclaration [style=filled, fillcolor="#FEFE62"];
      AxiomInclusion [style=filled, fillcolor="#FEFE62"];
      BoundVariable [style=filled, fillcolor="#FEFE62"];
      CompoundFormula [style=filled, fillcolor="#FEFE62"];
      Connective [style=filled, fillcolor="#FEFE62"];
      DefinitionDeclaration [style=filled, fillcolor="#FEFE62"];
      FreeVariable [style=filled, fillcolor="#FEFE62"];
      InferenceRuleDeclaration [style=filled, fillcolor="#FEFE62"];
      SimpleObjct [style=filled, fillcolor="#FEFE62"];
      Statement [style=filled, fillcolor="#FEFE62"];
      TheoryDerivation [style=filled, fillcolor="#FEFE62"];
      UniverseOfDiscourse [style=filled, fillcolor="#FEFE62"];
      Variable [style=filled, fillcolor="#FEFE62"];
      DefinitionInclusion [style=filled, fillcolor="#FEFE62"];
      FormulaStatement [style=filled, fillcolor="#FEFE62"];
      Hypothesis [style=filled, fillcolor="#FEFE62"];
      InferenceRuleInclusion [style=filled, fillcolor="#FEFE62"];
      ModusPonensInclusion [style=filled, fillcolor="#FEFE62"];
      ModusTollensInclusion [style=filled, fillcolor="#FEFE62"];
      ModusPonensDeclaration [style=filled, fillcolor="#FEFE62"];
      ModusTollensDeclaration [style=filled, fillcolor="#FEFE62"];
      InferredStatement [style=filled, fillcolor="#FEFE62"];

      AtheoreticalObject [style=dashed];
      NoteInclusion [style=dashed];

      "SymbolicObject" -> "AtheoreticalObject";
      "SymbolicObject" -> "Formula";
      "Formula" -> "AxiomDeclaration";
      "Formula" -> "CompoundFormula";
      "Formula" -> "DefinitionDeclaration";
      "Formula" -> "InferenceRuleDeclaration";
      "Formula" -> "Connective";
      "Formula" -> "SimpleObjct";
      "Formula" -> "Statement";
      "Formula" -> "TheoryDerivation";
      "Formula" -> "UniverseOfDiscourse";
      "Formula" -> "Variable";
      "Variable" -> "BoundVariable";
      "Variable" -> "FreeVariable";
      "Statement" -> "AxiomInclusion";
      "Statement" -> "DefinitionInclusion";
      "Statement" -> "FormulaStatement";
      "Statement" -> "Hypothesis";
      "Statement" -> "InferenceRuleInclusion";
      "InferenceRuleInclusion" -> "ModusPonensInclusion";
      "InferenceRuleInclusion" -> "ModusTollensInclusion";
      "InferenceRuleDeclaration" -> "ModusPonensDeclaration";
      "InferenceRuleDeclaration" -> "ModusTollensDeclaration";
      "AtheoreticalObject" -> "NoteInclusion";
      "FormulaStatement" -> "InferredStatement";

   }