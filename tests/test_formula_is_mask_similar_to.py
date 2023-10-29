from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestFormulaIsMaskSimilarTo(TestCase):
    def test_formula_is_mask_similar_to_unary_connective(self):
        pu.configuration.echo_axiom_declaration = True
        u = pu.UniverseOfDiscourse()
        r1a = u.r.declare(1)
        r1b = u.r.declare(1)
        o1 = u.o.declare()
        o2 = u.o.declare()
        phi1a = u.f(r1a, o1)
        with u.with_variable() as x:
            phi1b = u.f(r1a, x)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi=phi1b, mask={x}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi=phi1a, mask={x}))
        with u.with_variable() as x:
            phi1c = u.f(r1b, x)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi=phi1c, mask={x}))
            self.assertFalse(phi1c.is_masked_formula_similar_to(phi=phi1a, mask={x}))
        with u.with_variable() as x:
            phi1d = u.f(x, o1)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi=phi1d, mask={x}))
            self.assertTrue(phi1d.is_masked_formula_similar_to(phi=phi1a, mask={x}))
        with u.with_variable() as x:
            phi1e = u.f(x, o2)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi=phi1e, mask={x}))
            self.assertFalse(phi1e.is_masked_formula_similar_to(phi=phi1a, mask={x}))

    def test_formula_is_mask_similar_to_binary_connective(self):
        pu.configuration.echo_axiom_declaration = True
        u = pu.UniverseOfDiscourse()
        r1a = u.r.declare(2)
        r1b = u.r.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        phi1a = u.f(r1a, o1, o2)
        with u.with_variable() as x, u.with_variable() as y:
            phi1b = u.f(r1a, x, y)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x, y}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x, y}))
        with u.with_variable() as x, u.with_variable() as y:
            phi1c = u.f(r1b, x, y)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1c, {x, y}))
            self.assertFalse(phi1c.is_masked_formula_similar_to(phi1a, {x, y}))
        with u.with_variable() as x, u.with_variable() as y, u.with_variable() as z:
            phi1d = u.f(r1b, x, z)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1d, {x, y}))
            self.assertFalse(phi1d.is_masked_formula_similar_to(phi1a, {x, y}))

    def test_formula_is_mask_similar_to_embedded(self):
        pu.configuration.echo_axiom_declaration = True
        u = pu.UniverseOfDiscourse()
        r1a = u.r.declare(2)
        r1b = u.r.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        phi1a = u.f(r1a, u.f(r1b, o2, o3), o3)
        with u.with_variable() as x, u.with_variable() as y:
            phi1b = u.f(r1a, u.f(r1b, x, o3), y)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x, y}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x, y}))
        phi1c = u.f(u.r.land, u.f(r1b, o1, o2), u.f(r1b, o2, o3))
        with u.with_variable() as x1, u.with_variable() as x2, u.with_variable() as x3:
            phi1d = u.f(u.r.land, u.f(r1b, x1, x2), u.f(r1b, x2, x3))
            self.assertTrue(phi1c.is_masked_formula_similar_to(phi1d, {x1, x2, x3}))
            self.assertTrue(phi1d.is_masked_formula_similar_to(phi1c, {x1, x2, x3}))

    def test_formula_is_mask_similar_to_for_modus_ponens(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_formula_statement(a=ap, p=u.f(r1, o1, o2), lock=False)
        phi2 = t.i.axiom_interpretation.infer_formula_statement(a=ap, p=u.f(r1, o2, o3), lock=False)
        antecedent_statement = t.i.ci.infer_formula_statement(phi1, phi2)
        antecedent = antecedent_statement.valid_proposition

        with u.with_variable() as x, u.with_variable() as y, u.with_variable() as z:
            variable_set = {x, y, z}
            implication = t.i.axiom_interpretation.infer_formula_statement(a=ap,
                p=u.f(u.r.implies, u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)), u.f(r1, x, z)),
                lock=True)
            antecedent_with_variables = implication.valid_proposition.parameters[0]
            self.assertTrue(
                antecedent_with_variables.is_masked_formula_similar_to(antecedent, variable_set))
            self.assertTrue(
                antecedent.is_masked_formula_similar_to(antecedent_with_variables, variable_set))
