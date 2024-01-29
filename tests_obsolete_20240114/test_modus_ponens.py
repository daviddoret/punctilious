from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestModusPonens(TestCase):

    def test_modus_ponens_without_variable(self):
        import sample.sample_modus_ponens as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(phi=r2(o3)))
        self.assertEqual('r2(o3)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₂(𝑜₃)', proposition_of_interest.rep_formula(pu.encodings.unicode_extended))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.modus_ponens.infer_formula_statement(p_implies_q=o3 | u.c1.implies | o2, p=o2)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.modus_ponens.infer_formula_statement(p_implies_q=o3 | u.c1.implies | o2, p=o3)
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)

    def test_modus_ponens_with_variables(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare(2, signal_proposition=True)
        t = u.t.declare()
        a = u.a.declare(random_data.random_sentence())
        ap = t.include_axiom(a)
        with u.with_variable() as x, u.with_variable() as y, u.with_variable() as z:
            p_implies_q = t.i.axiom_interpretation.infer_formula_statement(ap,
                                                                           (r1(x, y) | u.c1.land | r1(y,
                                                                                                      z)) | u.c1.implies | r1(
                                                                               x, z), echo=True, lock=False)
        t.i.axiom_interpretation.infer_formula_statement(a=ap, p=r1(o1, o2), lock=False)
        t.i.axiom_interpretation.infer_formula_statement(a=ap, p=r1(o2, o3), lock=True)
        p_prime = t.i.conjunction_introduction.infer_formula_statement(p=r1(o1, o2), q=r1(o2, o3), echo=True)
        p_implies_q_prime = t.i.variable_substitution.infer_formula_statement(p=p_implies_q, phi=u.c1.tupl(o1, o2, o3),
                                                                              echo=True)
        conclusion = t.i.mp.infer_formula_statement(p_implies_q_prime, p_prime, echo=True)
        self.assertEqual('r1(o1, o3)', conclusion.valid_proposition.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₃)', conclusion.valid_proposition.rep_formula(pu.encodings.unicode_extended))