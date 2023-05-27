import core

t = core.Theory(
    symbol='foundation theory', extended_theories=core.universe_of_discourse)

nla_01 = t.nla(
    'A theory is a... (define punctilious data model).')

# The (axiomatic) class of (axiomatic) classes
nla_02 = t.nla(
    'An (axiomatic) class is a collection of theoretical objects that are '
    'unambiguously defined by the axioms of the theory it belongs to.')

nla_03 = t.nla(
    'The class of classes is the class of all classes defined in the '
    'universe-of-discourse (TODO: Or foundation theory?).')
class_of_classes = t.o('class-of-classes')
element_of = t.r(
    2, '∈', formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
fa1 = t.fa(t.f(element_of, class_of_classes, class_of_classes), nla=nla_02)

nla_04 = t.nla('The theory-class is the class of all theories')
theory_class = t.o('theory-class')
fa2b = t.fa(t.f(element_of, theory_class, class_of_classes), nla=nla_02)
fa2c = t.fa(t.f(element_of, t, theory_class), nla=nla_02)
# TODO: Implement a trigger to automatically add a statement (t in theory-class)
#   for every existing and new theory that is declared?

# Truth values
nla_05 = t.nla(
    'truth-values is the class whose elements are '
    'the theoretical-objects truth and falsehood.')
falsehood = t.o('false')
truth = t.o('true')
truth_values = t.o('truth-values')
fa_06 = t.fa(t.f(element_of, truth_values, class_of_classes), nla=nla_03)
fa_07 = t.fa(t.f(element_of, truth, truth_values), nla=nla_03)
fa_08 = t.fa(t.f(element_of, falsehood, truth_values), nla=nla_03)

# foundation propositional relations
nla_09 = t.nla(
    'propositional-relations is the class whose elements are '
    'the relations: conjunction, disjunction, implication, and negation, '
    'and any relation defined from these.')
propositional_relations_class = t.o('propositional-relations-class')
t.fa(
    t.f(element_of, propositional_relations_class, class_of_classes),
    nla=nla_03)
conjunction = t.r(
    2, '∧', core.Formula.infix_operator_representation,
    signal_proposition=True)
disjunction = t.r(
    2, '∨', core.Formula.infix_operator_representation,
    signal_proposition=True)
implication = t.r(
    2, '⟹', core.Formula.infix_operator_representation,
    signal_proposition=True)
negation = t.r(
    1, '¬', core.Formula.prefix_operator_representation,
    signal_proposition=True)
t.fa(t.f(element_of, conjunction, propositional_relations_class), nla=nla_09)
t.fa(t.f(element_of, disjunction, propositional_relations_class), nla=nla_09)
t.fa(t.f(element_of, implication, propositional_relations_class), nla=nla_09)
t.fa(t.f(element_of, negation, propositional_relations_class), nla=nla_09)

nla_10 = t.nla(
    'propositions is a class whose elements are '
    'truth, falsehood, all elements of the theory-formula-statement class, '
    'whose relation is an element-of propositional-relations-class, '
    'and all theory-formula-statements whose relation is defined '
    'from these. Its elements are called propositions.')
proposition_class = t.o('proposition-class')
t.fa(t.f(element_of, truth, class_of_classes), nla=nla_10)
t.fa(t.f(element_of, falsehood, class_of_classes), nla=nla_10)

nla_20 = t.nla(
    'If P is a proposition, then either the statement P has truth value true,'
    'or the statement P has truth value falsehood.')
has_truth_value = t.r(
    2, 'is',
    formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
t.fa(t.f(has_truth_value, truth, truth), nla=nla_10)
t.fa(t.f(has_truth_value, falsehood, falsehood), nla=nla_10)

nla_30 = t.nla(
    '¬ is a unary relation. '
    'If P is a proposition and it has truth-value truth, '
    'then ¬P has-truth-value false. '
    'Conversely, if P is a proposition and it has truth-value falsehood, '
    'then ¬P has truth-value true.')

# DOUBLE-NEGATION
nla_09_50 = t.nla('If P has-truth-value t, ¬(¬(P)) has-truth-value t.')
p_09_51 = t.v()
t_09_52 = t.v()
fa_09_51 = t.fa(
    t.f(
        implication,
        t.f(has_truth_value, p_09_51, t_09_52),
        t.f(has_truth_value, t.f(negation, t.f(negation, p_09_51)), t_09_52)),
    nla=nla_09_50)

nla_40 = t.nla(
    'If T is a theory, and both P is valid and ¬P is valid in T, '
    'then this theory is an element of contradictory-theories class.')
contradictory_theories = t.o('contradictory-theories')
contradictory_statements = t.o('contradictory-statement')
phi = t.v()
t.fa(
    t.f(
        implication,
        t.f(
            conjunction, t.f(has_truth_value, phi, truth),
            t.f(has_truth_value, phi, falsehood)),
        t.f(element_of, phi, contradictory_statements)),
    nla_40)

_relation_declaration = t.r(2, 'relation-declaration')
_simple_objct_declaration = t.r(2, 'simple-objct-declaration')
_theory_declaration = t.r(2, 'theory-declaration')
_theory_extension = t.r(2, 'theory-extension')
_variable_declaration = t.r(2, 'variable-declaration')

t.prnt()

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
