"""foundation-system-1 is one possible foundation system for Punctilious."""

import core

u = core.UniverseOfDiscourse('𝒰')

ft = u.t(
    symbol=core.Symbol('foundation-system', 1),
    is_theory_foundation_system=True)

nla_01 = ft.nla(
    'A theory is a... (define punctilious data model).')

# The (axiomatic) class of (axiomatic) classes
nla_02 = ft.nla(
    'An (axiomatic) class is a collection of theoretical objects that are '
    'unambiguously defined by the axioms of the theory it belongs to.')

nla_03 = ft.nla(
    'The class of classes is the class of all classes defined in the '
    'universe-of-discourse (TODO: Or foundation theory?).')
class_of_classes = u.o('class-of-classes')
element_of = u.r(
    2, '∈', formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
fa1 = ft.fa(u.f(element_of, class_of_classes, class_of_classes), nla=nla_02)

nla_04 = ft.nla('The theory-class is the class of all theories')
theory_class = ft.o('theory-class')
fa2b = ft.fa(ft.f(element_of, theory_class, class_of_classes), nla=nla_02)
fa2c = ft.fa(ft.f(element_of, ft, theory_class), nla=nla_02)
# TODO: Implement a trigger to automatically add a statement (t in theory-class)
#   for every existing and new theory that is declared?

# Truth values
nla_05 = ft.nla(
    'truth-values is the class whose elements are '
    'the theoretical-objects truth and falsehood.')
falsehood = ft.o('false')
truth = ft.o('true')
truth_values = ft.o('truth-values')
fa_06 = ft.fa(ft.f(element_of, truth_values, class_of_classes), nla=nla_03)
fa_07 = ft.fa(ft.f(element_of, truth, truth_values), nla=nla_03)
fa_08 = ft.fa(ft.f(element_of, falsehood, truth_values), nla=nla_03)

# foundation propositional relations
nla_09 = ft.nla(
    'propositional-relations is the class whose elements are '
    'the relations: conjunction, disjunction, implication, and negation, '
    'and any relation defined from these.')
propositional_relations_class = ft.o('propositional-relations-class')
ft.fa(
    ft.f(element_of, propositional_relations_class, class_of_classes),
    nla=nla_03)
conjunction = ft.r(
    2, '∧', core.Formula.infix_operator_representation,
    signal_proposition=True)
disjunction = ft.r(
    2, '∨', core.Formula.infix_operator_representation,
    signal_proposition=True)
implication = ft.r(
    2, '⟹', core.Formula.infix_operator_representation,
    signal_proposition=True)
negation = ft.r(
    1, '¬', core.Formula.prefix_operator_representation,
    signal_proposition=True)
ft.fa(ft.f(element_of, conjunction, propositional_relations_class), nla=nla_09)
ft.fa(ft.f(element_of, disjunction, propositional_relations_class), nla=nla_09)
ft.fa(ft.f(element_of, implication, propositional_relations_class), nla=nla_09)
ft.fa(ft.f(element_of, negation, propositional_relations_class), nla=nla_09)

nla_10 = ft.nla(
    'propositions is a class whose elements are '
    'truth, falsehood, all elements of the theory-formula-statement class, '
    'whose relation is an element-of propositional-relations-class, '
    'and all theory-formula-statements whose relation is defined '
    'from these. Its elements are called propositions.')
proposition_class = ft.o('proposition-class')
ft.fa(ft.f(element_of, truth, class_of_classes), nla=nla_10)
ft.fa(ft.f(element_of, falsehood, class_of_classes), nla=nla_10)

nla_20 = ft.nla(
    'If P is a proposition, then either the statement P has truth value true,'
    'or the statement P has truth value falsehood.')
has_truth_value = ft.r(
    2, 'is',
    formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
ft.fa(ft.f(has_truth_value, truth, truth), nla=nla_10)
ft.fa(ft.f(has_truth_value, falsehood, falsehood), nla=nla_10)

nla_30 = ft.nla(
    '¬ is a unary relation. '
    'If P is a proposition and it has truth-value truth, '
    'then ¬P has-truth-value false. '
    'Conversely, if P is a proposition and it has truth-value falsehood, '
    'then ¬P has truth-value true.')

# DOUBLE-NEGATION
nla_09_50 = ft.nla('If P has-truth-value t, ¬(¬(P)) has-truth-value t.')
p_09_51 = ft.v()
t_09_52 = ft.v()
fa_09_51 = ft.fa(
    ft.f(
        implication,
        ft.f(has_truth_value, p_09_51, t_09_52),
        ft.f(
            has_truth_value, ft.f(negation, ft.f(negation, p_09_51)), t_09_52)),
    nla=nla_09_50)

nla_40 = ft.nla(
    'If T is a theory, and both P is valid and ¬P is valid in T, '
    'then this theory is an element of contradictory-theories class.')
contradictory_theories = ft.o('contradictory-theories')
contradictory_statements = ft.o('contradictory-statement')
phi = ft.v()
ft.fa(
    ft.f(
        implication,
        ft.f(
            conjunction, ft.f(has_truth_value, phi, truth),
            ft.f(has_truth_value, phi, falsehood)),
        ft.f(element_of, phi, contradictory_statements)),
    nla_40)

_relation_declaration = ft.r(2, 'relation-declaration')
_simple_objct_declaration = ft.r(2, 'simple-objct-declaration')
_theory_declaration = ft.r(2, 'theory-declaration')
_theory_extension = ft.r(2, 'theory-extension')
_variable_declaration = ft.r(2, 'variable-declaration')

# t.prnt()

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


# TODO: REINTEGRER CE QUI SUIT


def elaborate_foundation_theory():
    global commutativity_of_equality
    global equality
    global fls
    global foundation_theory
    global ft
    global implies
    global neg
    global tru

    foundation_theory = Theory(
        theory=universe_of_discourse, symbol='foundation-theory')
    ft = foundation_theory

    tru = ft.o('true', capitalizable=True, python_name='tru')
    fls = ft.o('false', capitalizable=True, python_name='fls')

    implies = ft.r(
        2, 'implies',
        formula_rep=Formula.infix_operator_representation,
        python_name='implies', signal_proposition=True)

    def elaborate_commutativity_of_equality():
        global commutativity_of_equality
        global equality
        global fls
        global foundation_theory
        global ft
        global implies
        global tru

        nla_1 = ft.nla(
            '= is a binary relation such that, given any two theoretical-objcts x and y, '
            'if x=y then y=x, and for every statement s, s is valid iif subst s is valid.')
        equality = ft.r(
            2, '=',
            formula_rep=Formula.infix_operator_representation,
            python_name='equal_operator',
            signal_proposition=True)

        x1 = ft.v()
        x2 = ft.v()
        x1_equal_x2 = ft.f(equality, x1, x2)
        x2_equal_x1 = ft.f(equality, x2, x1)
        commutativity_of_equality = ft.fa(
            ft.f(implies, x1_equal_x2, x2_equal_x1), nla_1)

    elaborate_commutativity_of_equality()

    def gen1():
        global commutativity_of_equality
        global equality
        global fls
        global foundation_theory
        global ft
        global implies
        global tru
        def1 = ft.nld(
            natural_language='substitution is the process that consists in taking 3 theoretical-object o, p and q, that may be a composed-object such as a formula, and replacing in there all occurences of p by q.')
        axiom2 = ft.nla(
            'If x = y, o = subst(o, x, y) where o, x, and y are theoretical-objcts.')
        subst = ft.r(
            arity=3, symbol='subst',
            signal_theoretical_morphism=True, implementation=substitute_xy)
        # if x = y, implies subst(o, x, y)
        x = ft.v()
        y = ft.v()
        o = ft.v()
        r1x1 = ft.f(implies, ft.f(equality, x, y), ft.f(subst, o, x, y))
        equality_substitution = ft.fa(r1x1, axiom2)

    gen1()


elaborate_foundation_theory()
