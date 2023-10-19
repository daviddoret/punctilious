from unittest import TestCase
import punctilious as pu


class TestProofByContradiction1(TestCase):
    def test_proof_by_contradiction_1(self):
        import sample.sample_proof_by_contradiction_1 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        f: pu.Relation = test.f
        h: pu.Relation = test.h
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to(o2=f(o1, o3)))
        self.assertEqual('f1(o1, o3)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑓₁(𝑜₁, 𝑜₃)', proposition_of_interest.rep_formula(pu.encodings.unicode))
        # Syntax error, first parameter
        h2: pu.Hypothesis = t1.pose_hypothesis(hypothesis_formula=f(o2, o3),
            subtitle='We pose the negation hypothesis')
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.proof_by_contradiction_1.infer_formula_statement(h=h2, inc_h=u.r.inc(h2))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Syntax error, second parameter
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.proof_by_contradiction_1.infer_formula_statement(h=h, inc_h=o2)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Validity error
        h3: pu.Hypothesis = t1.pose_hypothesis(hypothesis_formula=u.r.lnot(f(o2, o3)),
            subtitle='We pose the negation hypothesis')
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.proof_by_contradiction_1.infer_formula_statement(h=h3,
                inc_h=u.r.inc(h3.child_theory))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
