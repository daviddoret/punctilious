from unittest import TestCase
import punctilious as pu
import random_data


class TestEqualTermsSubstitution(TestCase):
    def test_ets(self):
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(
            ap, u.f(u.r.equal, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) = ◆₂(ℴ₃))', phi1.repr_formula())
        phi2 = t.i.axiom_interpretation.infer_statement(ap,
                                                        u.f(r1, u.f(r1, u.f(r1, u.f(r1, o1, o2), u.f(r1, o1, o2)), o2),
                                                            u.f(r2, u.f(r1, o1, o2))),
                                                        echo=True)
        self.assertEqual('◆₁(◆₁(◆₁(◆₁(ℴ₁, ℴ₂), ◆₁(ℴ₁, ℴ₂)), ℴ₂), ◆₂(◆₁(ℴ₁, ℴ₂)))', phi2.repr_formula())
        phi3 = t.i.ets.infer_statement(phi2, phi1, echo=True)
        self.assertEqual('◆₁(◆₁(◆₁(◆₂(ℴ₃), ◆₂(ℴ₃)), ℴ₂), ◆₂(◆₂(ℴ₃)))', phi3.repr_formula())
