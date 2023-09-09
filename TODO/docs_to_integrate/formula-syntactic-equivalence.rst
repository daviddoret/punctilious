.. _formula-syntactic-equivalence:

# _formula-syntactic-equivalence

## Definition

Two theoretical-objects :math:`o_1` and :math:`o_2` are formula-syntactically-equivalent if and only if:

* :math:`o_1` and :math:`o_2` are declared in the same universe-of-discourse,
* if :math:`o_1` and :math:`o_2` are formula or formula-statements, their relations are formula-equivalent,
* if :math:`o_1` and :math:`o_2` are formula or formula-statements, their parameters are pairwise formula-equivalent,
* if :math:`o_1` and :math:`o_2` are neither formula nor statements, :math:`o_1` and :math:`o_2` are definition-equal.

Note that :math:`o_1` may be a formula and :math:`o_2` a formula-statement, or vice-versa.

## Implementations

* `TheoreticalObjct.is_formula_syntactically_equivalent_to(self, o2: TheoreticalObject) -> bool`
* `Formula.is_formula_syntactically_equivalent_to(self, o2: TheoreticalObject) -> bool`
* `Statement.is_formula_syntactically_equivalent_to(self, o2: TheoreticalObject) -> bool`

## Note

Intuitively, syntactic-equivalence state that two formula express the same thing with **the same symbols**. But note
that multiple distinct objects in a universe-of-discourse may be syntactically-equivalent but be denoted with distinct
symbols (e.g. example 1 below).

If the universe-of-discourse contains homographs,

### Example 1:

Let :math:`\phi` be the formula (¬¬(P ⋁ Q)).
Let :math:`\psi` be the formula (¬¬(P ⋁ Q)).
:math:`\phi` and :math:`\psi` **are** formula-syntactically-equivalent.

### Example 2:

Let :math:`\phi` be the formula (¬¬P).
Let :math:`\psi` be the formula (P).
:math:`\phi` and :math:`\psi` **are not** formula-syntactically-equivalent.

## See also

* :ref:`definitional-equality <definitional-equality>`
* :ref:`homography <homography>`
