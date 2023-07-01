from unittest import TestCase
import punctilious as pu
import random_data


class TestModusPonens(TestCase):

    def test_modus_ponens_without_variable(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t('test_modus_ponens_without_variable')
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        p_formula = u.f(r1, o1)
        self.assertEqual('◆₁(ℴ₁)', p_formula.rep_formula())
        q_formula = u.f(r2, o2)
        self.assertEqual('◆₂(ℴ₂)', q_formula.rep_formula())
        p_implies_q = t.i.axiom_interpretation.infer_statement(ap, u.f(u.r.implies, p_formula,
                                                                       q_formula))
        p_statement = t.i.axiom_interpretation.infer_statement(ap, p_formula)
        mp = t.i.mp.infer_statement(p_implies_q, p_statement)
        self.assertEqual('◆₂(ℴ₂)', mp.valid_proposition.rep_formula())

    def test_modus_ponens_with_free_variables(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t('test_modus_ponens_with_free_variables')
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        with u.v() as x, u.v() as y, u.v() as z:
            p_implies_q = t.i.axiom_interpretation.infer_statement(
                ap,
                u.f(
                    u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)), echo=True)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1, o2))
        phi2 = t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o2, o3))
        p_prime = t.i.ci.infer_statement(phi1, phi2, echo=True)
        p_implies_q_prime = t.i.vs.infer_statement(p_implies_q, o1, o2, o3, echo=True)
        conclusion = t.i.mp.infer_statement(p_implies_q_prime, p_prime, echo=True)
        self.assertEqual('◆₁(ℴ₁, ℴ₃)', conclusion.valid_proposition.rep_formula())
