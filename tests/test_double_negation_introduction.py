from unittest import TestCase
import punctilious as p
import random_data


class TestBiconditionalIntroduction(TestCase):
    def test_biconditional_introduction(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        r1 = u.r(2, signal_proposition=True)
        t = u.t(
            'testing-theory',
            include_double_negation_introduction_inference_rule=True)
        a = t.a('The arbitrary axiom of testing.')
        phi1 = t.dai(u.f(r1, o1, o2), a=a)
        phi2 = t.dni(phi1)
        self.assertEqual(
            '¬(¬(◆(ℴ₁, ℴ₂)))', phi2.repr())
