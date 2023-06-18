import core

t = core.TheoryElaborationSequence('classical propositional logic')

# Simple-objcts
falsehood = t.o('false')
truth = t.o('true')
proposition_class = t.o('proposition-class')

# Relations
conjunction = t.r(
    2, '∧', core.Formula.infix_operator_representation,
    signal_proposition=True)
disjunction = t.r(
    2, '∨', core.Formula.infix_operator_representation,
    signal_proposition=True)
has_truth_value = t.r(
    2, 'is', core.Formula.infix_operator_representation,
    signal_proposition=True)
implication = t.r(
    2, '⟹', core.Formula.infix_operator_representation,
    signal_proposition=True)
negation = t.r(
    1, '¬', core.Formula.prefix_operator_representation,
    signal_proposition=True)

"""
IDEAS:
- When the theory is extended, then it should equip the extended theory
  with constraints.
  
  Constraints:
  if phi is a classical-proposition-logic proposition,
  which is stated as phi is-a proposition
  then either phi is true or phi is false
  if phi is true and phi is false, this is a contradiction
  
"""
