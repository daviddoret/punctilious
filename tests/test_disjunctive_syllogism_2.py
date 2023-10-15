from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDisjunctiveSyllogism2(TestCase):
    def test_disjunctive_syllogism_2(self):
        import sample.sample_disjunctive_syllogism_2 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryElaborationSequence = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        o4: pu.SimpleObjct = test.o4
        theory_axiom: pu.AxiomInclusion = test.theory_axiom
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            o2=o1 | u.r.implies | o3))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.disjunctive_syllogism_2.infer_formula_statement(
                p_or_q=(o1 | u.r.implies | o2) | u.r.lor | (o3 | u.r.implies | o4),
                not_q=u.r.lnot(o1 | u.r.implies | o4))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.disjunctive_syllogism_2.infer_formula_statement(
                p_or_q=(o1 | u.r.implies | o2) | u.r.lor | (o3 | u.r.implies | o4),
                not_q=u.r.lnot(o3 | u.r.implies | o4))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
