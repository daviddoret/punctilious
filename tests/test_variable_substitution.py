from unittest import TestCase
import punctilious as pu
import random_data


class TestVariableSubstitution(TestCase):

    def test_variable_substitution_without_variable(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(2, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        p_formula = u.f(r1, u.f(r2, o1, o2))
        p_statement = t.i.axiom_interpretation.infer_statement(ap, p_formula, echo=True)
        # y_sequence = tuple()
        p_prime = t.i.vs.infer_statement(p_statement, echo=True)
        self.assertEqual('𝑟₁(𝑟₂(𝑜₁, 𝑜₂))', p_prime.rep_formula(text_format=pu.encodings.unicode))

    def test_variable_substitution_with_free_variables(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        o4 = u.o.declare()
        o5 = u.o.declare()
        o6 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(2, signal_proposition=True)
        t = u.t('test_variable_substitution_with_free_variables')
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        with u.v() as x, u.v() as y, u.v() as z:
            p_formula = u.f(r1, u.f(r2, u.f(r2, z, u.f(r2, u.f(r1, x), y)), u.f(r2, x, y)))
        p_statement = t.i.axiom_interpretation.infer_statement(ap, p_formula, echo=True)
        y_sequence = (o4, o6, o5)  # sequence: (z, x, y)
        p_prime = t.i.vs.infer_statement(p_statement, *y_sequence, echo=True)
        self.assertEqual('◆₁(◆₂(◆₂(ℴ₄, ◆₂(◆₁(ℴ₆), ℴ₅)), ◆₂(ℴ₆, ℴ₅)))', p_prime.rep_formula())
