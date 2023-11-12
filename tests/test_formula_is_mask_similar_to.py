from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestFormulaIsMaskSimilarTo(TestCase):
    def test_formula_is_mask_similar_to_unary_connective(self):
        pu.configuration.echo_axiom_declaration = True
        u = pu.UniverseOfDiscourse()
        r1a = u.c1.declare(1)
        r1b = u.c1.declare(1)
        o1 = u.o.declare()
        o2 = u.o.declare()
        phi1a = u.declare_compound_formula(r1a, o1)
        with u.with_variable() as x:
            phi1b = u.declare_compound_formula(r1a, x)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi=phi1b, mask={x}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi=phi1a, mask={x}))
        with u.with_variable() as x:
            phi1c = u.declare_compound_formula(r1b, x)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi=phi1c, mask={x}))
            self.assertFalse(phi1c.is_masked_formula_similar_to(phi=phi1a, mask={x}))
        with u.with_variable() as x:
            phi1d = u.declare_compound_formula(x, o1)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi=phi1d, mask={x}))
            self.assertTrue(phi1d.is_masked_formula_similar_to(phi=phi1a, mask={x}))
        with u.with_variable() as x:
            phi1e = u.declare_compound_formula(x, o2)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi=phi1e, mask={x}))
            self.assertFalse(phi1e.is_masked_formula_similar_to(phi=phi1a, mask={x}))

    def test_formula_is_mask_similar_to_binary_connective(self):
        pu.configuration.echo_axiom_declaration = True
        u = pu.UniverseOfDiscourse()
        r1a = u.c1.declare(2)
        r1b = u.c1.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        phi1a = u.declare_compound_formula(r1a, o1, o2)
        with u.with_variable() as x, u.with_variable() as y:
            phi1b = u.declare_compound_formula(r1a, x, y)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x, y}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x, y}))
        with u.with_variable() as x, u.with_variable() as y:
            phi1c = u.declare_compound_formula(r1b, x, y)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1c, {x, y}))
            self.assertFalse(phi1c.is_masked_formula_similar_to(phi1a, {x, y}))
        with u.with_variable() as x, u.with_variable() as y, u.with_variable() as z:
            phi1d = u.declare_compound_formula(r1b, x, z)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1d, {x, y}))
            self.assertFalse(phi1d.is_masked_formula_similar_to(phi1a, {x, y}))

    def test_formula_is_mask_similar_to_embedded(self):
        pu.configuration.echo_axiom_declaration = True
        u = pu.UniverseOfDiscourse()
        r1a = u.c1.declare(2)
        r1b = u.c1.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        phi1a = u.declare_compound_formula(r1a, u.declare_compound_formula(r1b, o2, o3), o3)
        with u.with_variable() as x, u.with_variable() as y:
            phi1b = u.declare_compound_formula(r1a, u.declare_compound_formula(r1b, x, o3), y)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x, y}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x, y}))
        phi1c = u.declare_compound_formula(u.c1.land, u.declare_compound_formula(r1b, o1, o2),
            u.declare_compound_formula(r1b, o2, o3))
        with u.with_variable() as x1, u.with_variable() as x2, u.with_variable() as x3:
            phi1d = u.declare_compound_formula(u.c1.land, u.declare_compound_formula(r1b, x1, x2),
                u.declare_compound_formula(r1b, x2, x3))
            self.assertTrue(phi1c.is_masked_formula_similar_to(phi1d, {x1, x2, x3}))
            self.assertTrue(phi1d.is_masked_formula_similar_to(phi1c, {x1, x2, x3}))

    def test_formula_is_mask_similar_to_for_modus_ponens(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare(2, signal_proposition=True)
        t = u.declare_theory()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_formula_statement(a=ap, p=u.declare_compound_formula(r1, o1, o2),
            lock=False)
        phi2 = t.i.axiom_interpretation.infer_formula_statement(a=ap, p=u.declare_compound_formula(r1, o2, o3),
            lock=False)
        antecedent_statement = t.i.ci.infer_formula_statement(phi1, phi2)
        antecedent = antecedent_statement.valid_proposition

        with u.with_variable() as x, u.with_variable() as y, u.with_variable() as z:
            variable_set = {x, y, z}
            implication = t.i.axiom_interpretation.infer_formula_statement(a=ap,
                p=u.declare_compound_formula(u.c1.implies,
                    u.declare_compound_formula(u.c1.land, u.declare_compound_formula(r1, x, y),
                        u.declare_compound_formula(r1, y, z)), u.declare_compound_formula(r1, x, z)), lock=True)
            antecedent_with_variables = implication.valid_proposition.terms[0]
            self.assertTrue(antecedent_with_variables.is_masked_formula_similar_to(antecedent, variable_set))
            self.assertTrue(antecedent.is_masked_formula_similar_to(antecedent_with_variables, variable_set))

    def test_formula_is_mask_similar_with_variables_and_object_references(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare()
        r2 = u.c1.declare()
        with u.with_variable('x') as x:
            phi1: pu.Formula = o1 | r1 | x
            phi2: pu.Formula = o1 | r1 | o2
            self.assertTrue(phi1.is_masked_formula_similar_to(phi=phi1, mask={}))
            self.assertTrue(phi2.is_masked_formula_similar_to(phi=phi2, mask={}))
            self.assertFalse(phi1.is_masked_formula_similar_to(phi=phi2, mask={}))
            self.assertFalse(phi2.is_masked_formula_similar_to(phi=phi1, mask={}))
            self.assertTrue(phi1.is_masked_formula_similar_to(phi=phi1, mask={x}))
            self.assertTrue(phi2.is_masked_formula_similar_to(phi=phi2, mask={x}))
            self.assertTrue(phi1.is_masked_formula_similar_to(phi=phi2, mask={x}))
            self.assertTrue(phi2.is_masked_formula_similar_to(phi=phi1, mask={x}))
        phi3: pu.Formula = o1 | r1 | u.c1.object_reference(x)
        self.assertTrue(phi3.is_masked_formula_similar_to(phi=phi3, mask={}))
        self.assertFalse(phi3.is_masked_formula_similar_to(phi=phi1, mask={}))
        self.assertFalse(phi3.is_masked_formula_similar_to(phi=phi2, mask={}))
        self.assertTrue(phi3.is_masked_formula_similar_to(phi=phi3, mask={x}))
        self.assertTrue(phi3.is_masked_formula_similar_to(phi=phi1, mask={x}))
        self.assertFalse(phi3.is_masked_formula_similar_to(phi=phi2, mask={x}))
