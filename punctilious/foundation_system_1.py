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
theory_class = u.o('theory-class')
fa2b = ft.fa(u.f(element_of, theory_class, class_of_classes), nla=nla_02)
fa2c = ft.fa(u.f(element_of, ft, theory_class), nla=nla_02)
# TODO: Implement a trigger to automatically add a statement (t in theory-class)
#   for every existing and new theory that is declared?

# Truth values
nla_05 = ft.nla(
    'truth-values is the class whose elements are '
    'the theoretical-objects truth and falsehood.')
falsehood = u.o('false')
truth = u.o('true')
truth_values = u.o('truth-values')
fa_06 = ft.fa(u.f(element_of, truth_values, class_of_classes), nla=nla_03)
fa_07 = ft.fa(u.f(element_of, truth, truth_values), nla=nla_03)
fa_08 = ft.fa(u.f(element_of, falsehood, truth_values), nla=nla_03)

# foundation propositional relations
nla_09 = ft.nla(
    'propositional-relations is the class whose elements are '
    'the relations: conjunction, disjunction, implication, and negation, '
    'and any relation defined from these.')
propositional_relations_class = u.o('propositional-relations-class')
ft.fa(
    u.f(element_of, propositional_relations_class, class_of_classes),
    nla=nla_03)
ft.equality = u.r(
    2, '=',
    formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)

ft.implication = u.r(
    2, '⟹', core.Formula.infix_operator_representation,
    signal_proposition=True)

conjunction = u.r(
    2, '∧', core.Formula.infix_operator_representation,
    signal_proposition=True)
disjunction = u.r(
    2, '∨', core.Formula.infix_operator_representation,
    signal_proposition=True)
ft.negation = u.r(
    1, '¬', core.Formula.prefix_operator_representation,
    signal_proposition=True)
ft.inequality = u.r(
    2, '≠', core.Formula.infix_operator_representation,
    signal_proposition=True)
ft.inequality.prnt()

ft.fa(u.f(element_of, conjunction, propositional_relations_class), nla=nla_09)
ft.fa(u.f(element_of, disjunction, propositional_relations_class), nla=nla_09)
ft.fa(
    u.f(element_of, ft.implication, propositional_relations_class), nla=nla_09)
ft.fa(
    u.f(element_of, ft.negation, propositional_relations_class),
    nla=nla_09).prnt(expanded=True)
ft.fa(
    u.f(element_of, ft.inequality, propositional_relations_class),
    nla=nla_09).prnt(expanded=True)
nla_01b = ft.nla(
    '= is a binary relation such that, given any two theoretical-objcts x and y, '
    'if x=y then y=x, and for every statement s, s is valid iif subst s is valid.')
with u.v('x') as x1, u.v('y') as x2:
    x1_equal_x2 = u.f(ft.equality, x1, x2)
    x2_equal_x1 = u.f(ft.equality, x2, x1)
    ft.commutativity_of_equality = ft.fa(
        u.f(ft.implication, x1_equal_x2, x2_equal_x1), nla_01b)

nld_55 = ft.nld('Inequality is defined as the negation of equality.')
with u.v('x') as x, u.v('y') as y:
    u.f(ft.inequality, x, y).prnt(expanded=True)
    u.f(ft.equality, x, y).prnt(expanded=True)
    u.f(ft.negation, u.f(ft.equality, x, y)).prnt(expanded=True)
    fd_55 = ft.fd(
        valid_proposition=
        u.f(
            ft.equality,
            u.f(ft.inequality, x, y),
            u.f(ft.negation, u.f(ft.equality, x, y))), nld=nld_55)
    fd_55.prnt()

nla_10 = ft.nla(
    'propositions is a class whose elements are '
    'truth, falsehood, all elements of the theory-formula-statement class, '
    'whose relation is an element-of propositional-relations-class, '
    'and all theory-formula-statements whose relation is defined '
    'from these. Its elements are called propositions.')
proposition_class = u.o('proposition-class')
ft.fa(u.f(element_of, truth, class_of_classes), nla=nla_10)
ft.fa(u.f(element_of, falsehood, class_of_classes), nla=nla_10)

nla_20 = ft.nla(
    'If P is a proposition, then either the statement P has truth value true,'
    'or the statement P has truth value falsehood.')
has_truth_value = u.r(
    2, 'is',
    formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
ft.fa(u.f(has_truth_value, truth, truth), nla=nla_10)
ft.fa(u.f(has_truth_value, falsehood, falsehood), nla=nla_10)

nla_30 = ft.nla(
    '¬ is a unary relation. '
    'If P is a proposition and it has truth-value truth, '
    'then ¬P has-truth-value false. '
    'Conversely, if P is a proposition and it has truth-value falsehood, '
    'then ¬P has truth-value true.')

# DOUBLE-NEGATION
nla_09_50 = ft.nla('If P has-truth-value t, ¬(¬(P)) has-truth-value t.')
with u.v() as p, u.v() as t:
    fa_09_51 = ft.fa(
        u.f(
            ft.implication,
            u.f(has_truth_value, p, t),
            u.f(
                has_truth_value, u.f(ft.negation, u.f(ft.negation, p)),
                t)),
        nla=nla_09_50)

nla_40 = ft.nla(
    'If T is a theory, and both P is valid and ¬P is valid in T, '
    'then this theory is an element of contradictory-theories class.')
contradictory_theories = u.o('contradictory-theories')
contradictory_statements = u.o('contradictory-statement')
with u.v('φ') as phi:
    ft.fa(
        u.f(
            ft.implication,
            u.f(
                conjunction, u.f(has_truth_value, phi, truth),
                u.f(has_truth_value, phi, falsehood)),
            u.f(element_of, phi, contradictory_statements)),
        nla_40)

_relation_declaration = u.r(2, 'relation-declaration')
_simple_objct_declaration = u.r(2, 'simple-objct-declaration')
_theory_declaration = u.r(2, 'theory-declaration')
_theory_extension = u.r(2, 'theory-extension')
_variable_declaration = u.r(2, 'variable-declaration')

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
    global fls
    global neg
    global tru

    tru = u.o('true', capitalizable=True, python_name='tru')
    fls = u.o('false', capitalizable=True, python_name='fls')

    def gen1():
        global fls
        global foundation_theory
        global tru
        def1 = ft.nld(
            natural_language='substitution is the process that consists in taking 3 theoretical-object o, p and q, that may be a composed-object such as a formula, and replacing in there all occurences of p by q.')
        axiom2 = ft.nla(
            'If x = y, o = subst(o, x, y) where o, x, and y are theoretical-objcts.')
        subst = u.r(
            arity=3, symbol='subst',
            signal_theoretical_morphism=True, implementation=substitute_xy)
        # if x = y, implies subst(o, x, y)
        x = u.v()
        y = u.v()
        o = u.v()
        r1x1 = u.f(implies, u.f(equality, x, y), u.f(subst, o, x, y))
        equality_substitution = ft.fa(r1x1, axiom2)

    gen1()


ft.prnt()

# elaborate_foundation_theory()
pass
