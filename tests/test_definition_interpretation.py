from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDefinitionInterpretation(TestCase):

    def test_definition_interpretation_1(self):
        import sample.sample_definition_interpretation as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        d: pu.DefinitionInclusion = test.theory_definition
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to((r1(o1, o2) | u.c1.equal | r2(o3))))
        self.assertEqual('(r1(o1, o2) = r2(o3))', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.definition_interpretation.infer_formula_statement(d=r2(o1), x=o1, y=o3)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Validity error  # with self.assertRaises(pu.PunctiliousException) as error:  #    definition_2 = u.declare_definition('Some definition')  #    t1.i.definition_interpretation.infer_formula_statement(a=definition_2, p=r1(o1, o3))  # self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,  #    error.exception.error_code)
        # Validity error - lock
        d.locked = True
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.definition_interpretation.infer_formula_statement(d=d, x=o1, y=o3)
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)
