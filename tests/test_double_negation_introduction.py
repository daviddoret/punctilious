from unittest import TestCase
import punctilious as pu
import random_data


class TestDoubleNegationIntroduction(TestCase):
    def test_dni(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse('test-dni-universe')
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t('test-dni-theory')
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1, o2))
        self.assertEqual(
            '◆₁(ℴ₁, ℴ₂)', phi1.rep())
        print(u.inference_rules.double_negation_introduction)
        print(t.inference_rule_inclusions.double_negation_introduction)
        phi2 = t.i.dni.infer_statement(phi1)
        self.assertEqual(
            '¬(¬(◆₁(ℴ₁, ℴ₂)))', phi2.rep())
        phi3 = t.i.dne.infer_statement(phi2)
        self.assertEqual(
            '◆₁(ℴ₁, ℴ₂)', phi3.rep())
        self.assertTrue(phi1.is_formula_equivalent_to(phi3))
