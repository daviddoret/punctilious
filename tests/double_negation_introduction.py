from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDoubleNegationIntroduction(TestCase):
    def test_dni_success(self):
        import sample as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        r1: pu.Relation = test.r1
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            o2=u.r.lnot(u.r.lnot(r1(o1, o2)))))
        self.assertEqual('not(not(r1(o1, o2)))',
            proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('¬(¬(𝑟₁(𝑜₁, 𝑜₂)))',
            proposition_of_interest.rep_formula(pu.encodings.unicode))

    def test_dni_failure(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, r1(o1, o2))
        self.assertEqual('r1(o1, o2)', phi1.rep_formula(encoding=pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₂)', phi1.rep_formula(encoding=pu.encodings.unicode))
        print(u.inference_rules.double_negation_introduction)
        print(t.inference_rule_inclusions.double_negation_introduction)
        # Trying to pass a formula that is not a valid formula-statement must raise an Exception
        with self.assertRaises(pu.FailedVerificationException):
            phi2 = t.i.dni.infer_statement(p=r1(o1, o3))
