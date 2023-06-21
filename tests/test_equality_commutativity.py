from unittest import TestCase
import punctilious as pu
import random_data


class TestEqualityCommutativity(TestCase):
    def test_ec(self):
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
        phi1 = t.dai(u.f(u.r.equal, u.f(r1, o1, o2), u.f(r2, o3)), ap=ap)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) = ◆₂(ℴ₃))', phi1.repr_as_formula())
        phi2 = t.i.ec.infer_statement(phi1, echo=True)
        self.assertEqual('(◆₂(ℴ₃) = ◆₁(ℴ₁, ℴ₂))', phi2.repr_as_formula())
