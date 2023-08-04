"""foundation-system-1 is one possible foundation system for Punctilious."""
import core
import repm

u = core.UniverseOfDiscourse()
ft = u.t(nameset=core.NameSet(symbol='foundation-theory-1'))

axiom_01 = ft.include_axiom(u.declare_axiom(
    'A theory is a... (define punctilious data model).'))

# The (axiomatic) class of (axiomatic) classes
axiom_02 = ft.include_axiom(u.declare_axiom(
    'An (axiomatic) class is a collection of theoretical objects that are '
    'unambiguously defined by the axioms of the theory it belongs to.'))

axiom_03 = ft.include_axiom(u.declare_axiom(
    'The class of classes is the class of all classes defined in the '
    'universe-of-discourse (TODO: Or foundation theory?).'))
class_of_classes = u.o.declare('class-of-classes')
element_of = u.r.declare(
    2, '∈', formula_rep=core.Formula.infix,
    signal_proposition=True, dashed_name='element-of')
fa1 = ft.i.axiom_interpretation.infer_statement(axiom_02,
                                                u.f(element_of, class_of_classes, class_of_classes))

nla_04 = ft.include_axiom(u.declare_axiom('The theory-class is the class of all theory_packages'))
theory_class = u.o.declare('theory-class')
fa2b = ft.i.axiom_interpretation.infer_statement(axiom_02,
                                                 u.f(element_of, theory_class, class_of_classes))
fa2c = ft.i.axiom_interpretation.infer_statement(axiom_02, u.f(element_of, ft, theory_class))
# TODO: Implement a trigger to automatically add a statement (t in theory-class)
#   for every existing and new theory that is declared?

# Truth values
nla_05 = ft.include_axiom(u.declare_axiom(natural_language=
                                          'truth-values is the class whose elements are '
                                          'the theoretical-objects truth and falsehood.'))
falsehood = u.o.declare('false')
truth = u.o.declare('true')
truth_values = u.o.declare('truth-values')
proposition_060 = ft.i.axiom_interpretation.infer_statement(axiom_03,
                                                            u.f(element_of, truth_values,
                                                                class_of_classes))
proposition_070 = ft.i.axiom_interpretation.infer_statement(axiom_03,
                                                            u.f(element_of, truth, truth_values))
proposition_080 = ft.i.axiom_interpretation.infer_statement(axiom_03, u.f(element_of, falsehood,
                                                                          truth_values))

# foundation propositional relations
nla_09 = ft.include_axiom(u.declare_axiom(natural_language=
                                          'propositional-relations is the class whose elements are '
                                          'the relations: conjunction, disjunction, implication, and negation, '
                                          'and any relation defined from these.'))
propositional_relations_class = u.o.declare('propositional-relations-class')
ft.i.axiom_interpretation.infer_statement(axiom_03,
                                          u.f(element_of, propositional_relations_class,
                                              class_of_classes))

ft.i.axiom_interpretation.infer_statement(nla_09,
                                          u.f(element_of, u.r.conjunction,
                                              propositional_relations_class))
ft.i.axiom_interpretation.infer_statement(nla_09, u.f(element_of, u.r.disjunction,
                                                      propositional_relations_class))
ft.i.axiom_interpretation.infer_statement(nla_09,
                                          u.f(element_of, u.r.implication,
                                              propositional_relations_class))
ft.i.axiom_interpretation.infer_statement(nla_09,
                                          u.f(element_of, u.r.lnot, propositional_relations_class))
ft.i.axiom_interpretation.infer_statement(nla_09,
                                          u.f(element_of, u.r.neq, propositional_relations_class))
nla_01b = ft.include_axiom(u.declare_axiom(
    '= is a binary relation such that, given any two theoretical-objcts x and y, '
    'if x=y then y=x, and for every statement s, s is valid iif subst s is valid.'))
with u.v('x') as x1, u.v('y') as x2:
    x1_equal_x2 = u.f(u.r.equal, x1, x2)
    x2_equal_x1 = u.f(u.r.equal, x2, x1)
    ft.commutativity_of_equality = ft.i.axiom_interpretation.infer_statement(nla_01b,
                                                                             u.f(u.r.implication,
                                                                                 x1_equal_x2,
                                                                                 x2_equal_x1))

d_55 = u.declare_definition('Inequality is defined as the negation of equality.')
nld_55 = ft.include_definition(d=d_55)
with u.v('x') as x, u.v('y') as y:
    ft.i.definition_interpretation.infer_statement(
        nld_55,
        u.f(
            u.r.equal,
            u.f(u.r.neq, x, y),
            u.f(u.r.lnot, u.f(u.r.equal, x, y))))

nla_10 = ft.include_axiom(u.declare_axiom(
    'propositions is a class whose elements are '
    'truth, falsehood, all elements of the theory-formula-statement class, '
    'whose relation is an element-of propositional-relations-class, '
    'and all theory-formula-statements whose relation is defined '
    'from these. Its elements are called propositions.'))
proposition_class = u.o.declare('proposition-class')
ft.i.axiom_interpretation.infer_statement(nla_10, u.f(element_of, truth, class_of_classes))
ft.i.axiom_interpretation.infer_statement(nla_10, u.f(element_of, falsehood, class_of_classes))

nla_20 = ft.include_axiom(u.declare_axiom(
    'If P is a proposition, then either the statement P has truth value true,'
    'or the statement P has truth value falsehood.'))
has_truth_value = u.r.declare(
    2, 'is',
    formula_rep=core.Formula.infix,
    signal_proposition=True)
ft.i.axiom_interpretation.infer_statement(nla_10, u.f(has_truth_value, truth, truth))
ft.i.axiom_interpretation.infer_statement(nla_10, u.f(has_truth_value, falsehood, falsehood))

nla_30 = ft.include_axiom(u.declare_axiom(
    '¬ is a unary relation. '
    'If P is a proposition and it has truth-value truth, '
    'then ¬P has-truth-value false. '
    'Conversely, if P is a proposition and it has truth-value falsehood, '
    'then ¬P has truth-value true.'))

# DOUBLE-NEGATION
nla_09_50 = ft.include_axiom(u.declare_axiom('If P has-truth-value t, ¬(¬(P)) has-truth-value t.'))
with u.v() as p, u.v() as t:
    fa_09_51 = ft.i.axiom_interpretation.infer_statement(nla_09_50,
                                                         u.f(
                                                             u.r.implication,
                                                             u.f(has_truth_value, p, t),
                                                             u.f(
                                                                 has_truth_value,
                                                                 u.f(u.r.lnot, u.f(u.r.lnot, p)),
                                                                 t)))


# CONJUNCTION
def define_conjunction():
    nla_39 = ft.include_axiom(u.declare_axiom(
        'If P and Q are logical propositions, '
        '(P ∧ Q) is true if and only if '
        'both P and Q are true, '
        'otherwise it is false.'))


define_conjunction()


def section_200_theory_consistency():
    axiom_200 = ft.include_axiom(
        'If 𝓣 is a theory, '
        'if 𝝋 is a statement in 𝓣, '
        'and if ¬𝝋 is a statement in 𝓣, '
        'then 𝓣 is inconsistent.',
        title='Theory inconsistency')

    proposition_200_1 = u.implication_relation(u.f(u.im))


def define_biconditional():
    nla = ft.include_axiom(u.declare_axiom(natural_language=
                                           'If P and Q are logical propositions, '
                                           '(P ⇔ Q) is true if and only if '
                                           '((P ⇒ Q) ∧ (Q ⇒ P)), '
                                           'otherwise it is false.'))


define_biconditional()

nla_40 = ft.include_axiom(u.declare_axiom(natural_language=
                                          'If T is a theory, and both P is valid and ¬P is valid in T, '
                                          'then this theory is an element of contradictory-theory_packages class.'))
contradictory_theories = u.o.declare('contradictory-theory_packages')
contradictory_statements = u.o.declare('contradictory-statement')
with u.v('φ') as phi:
    ft.i.axiom_interpretation.infer_statement(nla_40,
                                              u.f(
                                                  u.r.implication,
                                                  u.f(
                                                      u.r.conjunction,
                                                      u.f(has_truth_value, phi, truth),
                                                      u.f(has_truth_value, phi, falsehood)),
                                                  u.f(element_of, phi, contradictory_statements)))

_relation_declaration = u.r.declare(2, 'relation-declaration')
_simple_objct_declaration = u.r.declare(2, 'simple-objct-declaration')
_theory_declaration = u.r.declare(2, 'theory-declaration')
_theory_extension = u.r.declare(2, 'theory-extension')
_variable_declaration = u.r.declare(2, 'variable-declaration')

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

    tru = u.o.declare('true', capitalizable=True, python_name='tru')
    fls = u.o.declare('false', capitalizable=True, python_name='fls')

    def gen1():
        global fls
        global foundation_theory
        global tru
        def1 = ft.d(
            natural_language='substitution is the process that consists in taking 3 theoretical-object o, p and q, that may be a composed-object such as a formula, and replacing in there all occurences of p by q.')
        axiom2 = ft.include_axiom(
            'If x = y, o = subst(o, x, y) where o, x, and y are theoretical-objcts.')
        subst = u.r.declare(
            arity=3, nameset='subst',
            signal_theoretical_morphism=True, implementation=substitute_xy)
        # if x = y, implies subst(o, x, y)
        x = u.v()
        y = u.v()
        o = u.v()
        r1x1 = u.f(implies, u.f(equality, x, y), u.f(subst, o, x, y))
        equality_substitution = ft.i.axiom_interpretation.infer_statement(axiom2, r1x1)

    gen1()


# ft.prnt()

# elaborate_foundation_theory()
pass

# print(ft.repr_as_theory())
foundation_system_1 = ft
