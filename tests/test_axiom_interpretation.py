from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestAxiomInterpretation(TestCase):

    def test_axiom_interpretation_1(self):
        import sample.sample_axiom_interpretation as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        a: pu.AxiomInclusion = test.theory_axiom
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to((r1(o1, o2) | u.c1.implies | r2(o3))))
        self.assertEqual('(r1(o1, o2) implies r2(o3))', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.axiom_interpretation.infer_formula_statement(a=r2(o1), p=r1(o1, o3))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Validity error  # with self.assertRaises(pu.PunctiliousException) as error:  #    axiom_2 = u.a.declare('Some axiom')  #    t1.i.axiom_interpretation.infer_formula_statement(a=axiom_2, p=r1(o1, o3))  # self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,  #    error.exception.error_code)
        # Validity error - lock
        a.locked = True
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.axiom_interpretation.infer_formula_statement(a=a, p=r1(o1, o3))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)

    def test_axiom_interpretation_2(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.unicode
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        # Prepare the universe-of-discourse
        a1 = u.a.declare(natural_language=random_data.random_sentence())
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.c1.declare(arity=2, signal_proposition=True)
        r2 = u.c1.declare(arity=1)
        phi1 = u.declare_compound_formula(r1, o1, o2)
        # Elaborate the theory
        t = u.declare_theory()
        a2 = t.include_axiom(a1)
        p1 = t.i.axiom_interpretation.infer_formula_statement(a2, phi1)
        self.assertTrue(
            p1.valid_proposition.is_formula_syntactically_equivalent_to(u.declare_compound_formula(r1, o1, o2)))
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t.i.axiom_interpretation.infer_formula_statement(a2, r2(o1))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)
