from unittest import TestCase
import punctilious as p
import random_data


class TestDoubleNegationIntroduction(TestCase):
    def test_dni(self):
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
        self.assertEqual(
            '◆(ℴ₁, ℴ₂)', phi1.repr())
        print(u.inference_rules.double_negation_introduction)
        print(t.inference_rule_inclusions.double_negation_introduction)
        phi2 = t.i.dni.infer_statement(phi1)
        self.assertEqual(
            '¬(¬(◆(ℴ₁, ℴ₂)))', phi2.repr())
        phi3 = t.i.dne.infer_statement(phi2)
        self.assertEqual(
            '◆(ℴ₁, ℴ₂)', phi3.repr())
        self.assertTrue(phi1.is_formula_equivalent_to(phi3))
