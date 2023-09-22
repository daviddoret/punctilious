from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestModusPonens(TestCase):

    def test_modus_ponens_without_variable(self):
        import sample.sample_modus_ponens as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(o2=r2(o3)))
        self.assertEqual('r2(o3)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₂(𝑜₃)', proposition_of_interest.rep_formula(pu.encodings.unicode))

    def test_modus_ponens_with_free_variables(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        with u.v() as x, u.v() as y, u.v() as z:
            p_implies_q = t.i.axiom_interpretation.infer_formula_statement(ap,
                (r1(x, y) | u.r.land | r1(y, z)) | u.r.implies | r1(x, z), echo=True)
        t.i.axiom_interpretation.infer_formula_statement(axiom=ap, formula=r1(o1, o2))
        t.i.axiom_interpretation.infer_formula_statement(axiom=ap, formula=r1(o2, o3))
        p_prime = t.i.conjunction_introduction.infer_formula_statement(p=r1(o1, o2), q=r1(o2, o3),
            echo=True)
        p_implies_q_prime = t.i.variable_substitution.infer_formula_statement(p=p_implies_q,
            phi=(o1, o2, o3), echo=True)
        conclusion = t.i.mp.infer_formula_statement(p_implies_q_prime, p_prime, echo=True)
        self.assertEqual('r1(o1, o3)',
            conclusion.valid_proposition.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₃)',
            conclusion.valid_proposition.rep_formula(pu.encodings.unicode))
