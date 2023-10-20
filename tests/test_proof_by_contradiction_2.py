from unittest import TestCase
import punctilious as pu


class TestProofByContradiction2(TestCase):
    def test_proof_by_contradiction_2(self):
        import sample.sample_proof_by_contradiction_2 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        h: pu.Hypothesis = test.h
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        pass
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to(phi=o1 | u.r.eq | o2))
        self.assertEqual('(o1 = o2)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑜₁ = 𝑜₂)', proposition_of_interest.rep_formula(pu.encodings.unicode))
        # Syntax error, first parameter
        f = u.r.declare(symbol='f', arity=2, signal_proposition=True)
        h2: pu.Hypothesis = t1.pose_hypothesis(hypothesis_formula=f(o1, o2),
            subtitle='We pose the negation hypothesis')
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.proof_by_contradiction_2.infer_formula_statement(h=h2, inc_h=u.r.inc(h2))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Syntax error, second parameter
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.proof_by_contradiction_2.infer_formula_statement(h=h, inc_h=f(o1, o2))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Validity error
        o3: pu.SimpleObjct = u.o.declare()
        h3: pu.Hypothesis = t1.pose_hypothesis(hypothesis_formula=o2 | u.r.unequal | o3,
            subtitle='We pose the negation hypothesis')
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.proof_by_contradiction_2.infer_formula_statement(h=h3,
                inc_h=u.r.inc(h3.child_theory))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
