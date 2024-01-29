from unittest import TestCase
import punctilious as pu


class TestAbsorption(TestCase):
    def test_absorption_1(self):
        import sample.sample_absorption as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            (r1(o1, o2) | u.c1.implies | (r1(o1, o2) | u.c1.land | r2(o3)))))
        self.assertEqual('(r1(o1, o2) implies (r1(o1, o2) and r2(o3)))',
                         proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ⊃ (𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃)))',
                         proposition_of_interest.rep_formula(pu.encodings.unicode_extended))

    def test_absorption_2_validity_error(self):
        import sample.sample_absorption as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.Formula = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        p_implies_q: pu.CompoundFormula = r1(o1, o3) | u.c1.implies | r2(o3)

        with self.assertRaises(pu.PunctiliousException) as context:
            proposition_error = t1.i.absorption.infer_formula_statement(p_implies_q=p_implies_q,
                                                                        subtitle='The proposition error')
            self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, context.exception.error_code)

    def test_absorption_3_syntax_error(self):
        import sample.sample_absorption as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        p_implies_q: pu.CompoundFormula = r1(o1, o2) | u.c1.iff | r2(o3)

        with self.assertRaises(pu.PunctiliousException) as context:
            proposition_error = t1.i.absorption.infer_formula_statement(p_implies_q=p_implies_q,
                                                                        subtitle='The proposition error')
            self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, context.exception.error_code)