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
        t = u.t('test_variable_substitution_without_variable')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        p_formula = u.f(r1, u.f(r2, o1, o2))
        p_statement = t.dai(p_formula, ap=ap, echo=True)
        y_sequence = tuple()
        p_prime = t.i.vs.infer_statement(p_statement, *y_sequence)

    def test_variable_substitution_with_free_variables(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t('test_variable_substitution_with_free_variables')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        with u.v() as x, u.v() as y, u.v() as z:
            implication = t.dai(
                u.f(
                    u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap, echo=True)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dai(u.f(r1, o2, o3), ap=ap)
        phi1_and_phi2 = t.i.ci.infer_statement(phi1, phi2, echo=True)
        conclusion_1 = t.i.mp.infer_statement(implication, phi1_and_phi2, echo=True)
        self.assertEqual('◆(ℴ₁, ℴ₃)', conclusion_1.valid_proposition.repr_as_formula())
