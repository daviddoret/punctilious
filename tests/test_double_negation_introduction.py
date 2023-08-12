from unittest import TestCase
import punctilious as pu
import random_data


class TestDoubleNegationIntroduction(TestCase):
    def test_dni(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1, o2))
        self.assertEqual('r1(o1, o2)', phi1.rep_formula(encoding=pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₂)', phi1.rep_formula(encoding=pu.encodings.unicode))
        print(u.inference_rules.double_negation_introduction)
        print(t.inference_rule_inclusions.double_negation_introduction)
        phi2 = t.i.dni.infer_statement(phi1)
        self.assertEqual('not(not(r1(o1, o2)))', phi2.rep_formula(encoding=pu.encodings.plaintext))
        self.assertEqual('¬(¬(𝑟₁(𝑜₁, 𝑜₂)))', phi2.rep_formula(encoding=pu.encodings.unicode))
        phi3 = t.i.dne.infer_statement(phi2)
        self.assertEqual('r1(o1, o2)', phi3.rep_formula(encoding=pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₂)', phi3.rep_formula(encoding=pu.encodings.unicode))
        self.assertTrue(phi1.is_formula_syntactically_equivalent_to(phi3))
