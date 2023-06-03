"""foundation-system-1 is one possible foundation system for Punctilious."""

import core
import repm

u = core.UniverseOfDiscourse()
ft = core.Theory(
    symbol='ℱ',
    is_theory_foundation_system=True, universe_of_discourse=u)

axiom_01 = ft.a(
    'A theory is a... (define punctilious data model).')

# The (axiomatic) class of (axiomatic) classes
axiom_02 = ft.a(
    'An (axiomatic) class is a collection of theoretical objects that are '
    'unambiguously defined by the axioms of the theory it belongs to.')

axiom_03 = ft.a(
    'The class of classes is the class of all classes defined in the '
    'universe-of-discourse (TODO: Or foundation theory?).')
class_of_classes = u.o('class-of-classes')
element_of = u.r(
    2, '∈', formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
fa1 = ft.dai(u.f(element_of, class_of_classes, class_of_classes), a=axiom_02)

nla_04 = ft.a('The theory-class is the class of all theories')
theory_class = u.o('theory-class')
fa2b = ft.dai(u.f(element_of, theory_class, class_of_classes), a=axiom_02)
fa2c = ft.dai(u.f(element_of, ft, theory_class), a=axiom_02)
# TODO: Implement a trigger to automatically add a statement (t in theory-class)
#   for every existing and new theory that is declared?

# Truth values
nla_05 = ft.a(
    'truth-values is the class whose elements are '
    'the theoretical-objects truth and falsehood.')
falsehood = u.o('false')
truth = u.o('true')
truth_values = u.o('truth-values')
proposition_060 = ft.dai(
    u.f(element_of, truth_values, class_of_classes), a=axiom_03)
proposition_070 = ft.dai(u.f(element_of, truth, truth_values), a=axiom_03)
proposition_080 = ft.dai(u.f(element_of, falsehood, truth_values), a=axiom_03)

# foundation propositional relations
nla_09 = ft.a(
    'propositional-relations is the class whose elements are '
    'the relations: conjunction, disjunction, implication, and negation, '
    'and any relation defined from these.')
propositional_relations_class = u.o('propositional-relations-class')
ft.dai(
    u.f(element_of, propositional_relations_class, class_of_classes),
    a=axiom_03)
ft.equality = u.r(
    2, '=',
    formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)

ft.implication = u.r(
    2, '⟹', core.Formula.infix_operator_representation,
    signal_proposition=True)


class ModusPonensStatement(core.FormulaStatement):
    """
    TODO: Make ModusPonens a subclass of InferenceRule.

    Definition:
    -----------
    A modus-ponens is a valid rule-of-inference propositional-logic argument that,
    given a proposition (P implies Q)
    given a proposition (P is True)
    infers the proposition (Q is True)

    Requirements:
    -------------
    The parent theory must expose the implication attribute.
    """

    def __init__(
        self, conditional, antecedent, symbol=None, category=None, theory=None,
        reference=None, title=None):
        category = core.statement_categories.proposition if category is None else category
        self.conditional = conditional
        self.antecedent = antecedent
        valid_proposition = ModusPonensInferenceRule.execute_algorithm(
            theory=theory, conditional=conditional, antecedent=antecedent)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof by modus ponens")}'
            output = output + f'\n\t{self.conditional.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.conditional.repr_as_ref())}.'
            output = output + f'\n\t{self.antecedent.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.antecedent.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class ModusPonensInferenceRule(core.InferenceRule):

    @staticmethod
    def infer(
        theory, conditional, antecedent, symbol=None, category=None,
        reference=None, title=None):
        """Given a conditional and an antecedent, infer a statement using the
        modus-ponens inference-rule in the theory."""
        return ModusPonensStatement(
            conditional=conditional, antecedent=antecedent, symbol=symbol,
            category=category, theory=theory, reference=reference, title=title)

    @staticmethod
    def execute_algorithm(theory, conditional, antecedent):
        """Execute the modus-ponens algorithm."""
        assert isinstance(theory, core.Theory)
        assert isinstance(conditional, core.FormulaStatement)
        assert theory.has_objct_in_hierarchy(conditional)
        assert theory.has_objct_in_hierarchy(antecedent)
        core.verify(
            isinstance(theory.implication, core.Relation),
            'The usage of the ModusPonens class in a theory requires the '
            'implication attribute in that theory.')
        assert conditional.valid_proposition.relation is theory.implication
        p_prime = conditional.valid_proposition.parameters[0]
        q_prime = conditional.valid_proposition.parameters[1]
        mask = p_prime.get_variable_set()
        # Check p consistency
        # If the p statement is present in the theory,
        # it necessarily mean that p is true,
        # because every statement in the theory is a valid proposition.
        assert isinstance(antecedent, core.FormulaStatement)
        similitude, _values = antecedent.valid_proposition._is_masked_formula_similar_to(
            o2=p_prime, mask=mask)
        assert antecedent.valid_proposition.is_masked_formula_similar_to(
            o2=p_prime, mask=mask)
        # Build q by variable substitution
        substitution_map = dict((v, k) for k, v in _values.items())
        valid_proposition = q_prime.substitute(
            substitution_map=substitution_map, target_theory=theory)
        return valid_proposition


ft.modus_ponens_inference_rule = ModusPonensInferenceRule

ft.conjunction = u.r(
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

ft.dai(
    u.f(element_of, ft.conjunction, propositional_relations_class), a=nla_09)
ft.dai(u.f(element_of, disjunction, propositional_relations_class), a=nla_09)
ft.dai(
    u.f(element_of, ft.implication, propositional_relations_class), a=nla_09)
ft.dai(
    u.f(element_of, ft.negation, propositional_relations_class),
    a=nla_09)
ft.dai(
    u.f(element_of, ft.inequality, propositional_relations_class),
    a=nla_09)
nla_01b = ft.a(
    '= is a binary relation such that, given any two theoretical-objcts x and y, '
    'if x=y then y=x, and for every statement s, s is valid iif subst s is valid.')
with u.v('x') as x1, u.v('y') as x2:
    x1_equal_x2 = u.f(ft.equality, x1, x2)
    x2_equal_x1 = u.f(ft.equality, x2, x1)
    ft.commutativity_of_equality = ft.dai(
        u.f(ft.implication, x1_equal_x2, x2_equal_x1), nla_01b)

nld_55 = ft.d('Inequality is defined as the negation of equality.')
with u.v('x') as x, u.v('y') as y:
    ft.ddi(
        valid_proposition=
        u.f(
            ft.equality,
            u.f(ft.inequality, x, y),
            u.f(ft.negation, u.f(ft.equality, x, y))), d=nld_55)

nla_10 = ft.a(
    'propositions is a class whose elements are '
    'truth, falsehood, all elements of the theory-formula-statement class, '
    'whose relation is an element-of propositional-relations-class, '
    'and all theory-formula-statements whose relation is defined '
    'from these. Its elements are called propositions.')
proposition_class = u.o('proposition-class')
ft.dai(u.f(element_of, truth, class_of_classes), a=nla_10)
ft.dai(u.f(element_of, falsehood, class_of_classes), a=nla_10)

nla_20 = ft.a(
    'If P is a proposition, then either the statement P has truth value true,'
    'or the statement P has truth value falsehood.')
has_truth_value = u.r(
    2, 'is',
    formula_rep=core.Formula.infix_operator_representation,
    signal_proposition=True)
ft.dai(u.f(has_truth_value, truth, truth), a=nla_10)
ft.dai(u.f(has_truth_value, falsehood, falsehood), a=nla_10)

nla_30 = ft.a(
    '¬ is a unary relation. '
    'If P is a proposition and it has truth-value truth, '
    'then ¬P has-truth-value false. '
    'Conversely, if P is a proposition and it has truth-value falsehood, '
    'then ¬P has truth-value true.')

# DOUBLE-NEGATION
nla_09_50 = ft.a('If P has-truth-value t, ¬(¬(P)) has-truth-value t.')
with u.v() as p, u.v() as t:
    fa_09_51 = ft.dai(
        u.f(
            ft.implication,
            u.f(has_truth_value, p, t),
            u.f(
                has_truth_value, u.f(ft.negation, u.f(ft.negation, p)),
                t)),
        a=nla_09_50)


# CONJUNCTION
def define_conjunction():
    nla_39 = ft.a(
        'If P and Q are logical propositions, '
        '(P ∧ Q) is true if and only if '
        'both P and Q are true, '
        'otherwise it is false.')


define_conjunction()


def section_200_theory_consistency():
    axiom_200 = ft.a(
        'If 𝓣 is a theory, '
        'if 𝝋 is a statement in 𝓣, '
        'and if ¬𝝋 is a statement in 𝓣, '
        'then 𝓣 is inconsistent.',
        title='Theory inconsistency')

    proposition_200_1 = ft.implication(u.f(u.im))


def define_biconditional():
    nla = ft.a(
        'If P and Q are logical propositions, '
        '(P ⇔ Q) is true if and only if '
        '((P ⇒ Q) ∧ (Q ⇒ P)), '
        'otherwise it is false.')


define_biconditional()

nla_40 = ft.a(
    'If T is a theory, and both P is valid and ¬P is valid in T, '
    'then this theory is an element of contradictory-theories class.')
contradictory_theories = u.o('contradictory-theories')
contradictory_statements = u.o('contradictory-statement')
with u.v('φ') as phi:
    ft.dai(
        u.f(
            ft.implication,
            u.f(
                ft.conjunction, u.f(has_truth_value, phi, truth),
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
        def1 = ft.d(
            natural_language='substitution is the process that consists in taking 3 theoretical-object o, p and q, that may be a composed-object such as a formula, and replacing in there all occurences of p by q.')
        axiom2 = ft.a(
            'If x = y, o = subst(o, x, y) where o, x, and y are theoretical-objcts.')
        subst = u.r(
            arity=3, symbol='subst',
            signal_theoretical_morphism=True, implementation=substitute_xy)
        # if x = y, implies subst(o, x, y)
        x = u.v()
        y = u.v()
        o = u.v()
        r1x1 = u.f(implies, u.f(equality, x, y), u.f(subst, o, x, y))
        equality_substitution = ft.dai(r1x1, axiom2)

    gen1()


# ft.prnt()

# elaborate_foundation_theory()
pass
