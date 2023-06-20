from unittest import TestCase
import punctilious as p
import random_data


class TestDoubleNegationElimination(TestCase):
    def test_dne(self):
        p.configuration.echo_default = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t('testing-theory')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        phi0 = u.f(r1, o1, o2)
        phi1 = t.dai(u.f(u.r.lnot, u.f(u.r.lnot, phi0)), ap=ap)
        self.assertEqual(
            '¬(¬(◆₁(ℴ₁, ℴ₂)))', phi1.repr())
        phi2 = t.i.dne.infer_statement(phi1)
        self.assertEqual(
            '◆₁(ℴ₁, ℴ₂)', phi2.repr())
        self.assertTrue(phi2.is_formula_equivalent_to(phi0))
