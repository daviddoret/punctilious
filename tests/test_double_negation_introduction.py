from unittest import TestCase
import punctilious as p
import random_data


class TestBiconditionalIntroduction(TestCase):
    def test_biconditional_introduction(self):
        p.configuration.echo_default = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t(
            'testing-theory',
            include_double_negation_introduction_inference_rule=True)
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dni(phi1)
        self.assertEqual(
            '¬(¬(◆(ℴ₁, ℴ₂)))', phi2.repr())
