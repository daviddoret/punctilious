from unittest import TestCase
import punctilious as p
import random_data


class TestFormulaIsMaskSimilarTo(TestCase):
    def test_formula_is_mask_similar_to_unary_relation(self):
        p.configuration.echo_axiom = True
        u = p.UniverseOfDiscourse('test_formula_is_mask_similar_to_unary_relation')
        r1a = u.r.declare(1)
        r1b = u.r.declare(1)
        o1 = u.o()
        o2 = u.o()
        phi1a = u.f(r1a, o1)
        with u.v() as x:
            phi1b = u.f(r1a, x)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x}))
        with u.v() as x:
            phi1c = u.f(r1b, x)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1c, {x}))
            self.assertFalse(phi1c.is_masked_formula_similar_to(phi1a, {x}))
        with u.v() as x:
            phi1d = u.f(x, o1)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1d, {x}))
            self.assertTrue(phi1d.is_masked_formula_similar_to(phi1a, {x}))
        with u.v() as x:
            phi1e = u.f(x, o2)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1e, {x}))
            self.assertFalse(phi1e.is_masked_formula_similar_to(phi1a, {x}))

    def test_formula_is_mask_similar_to_binary_relation(self):
        p.configuration.echo_axiom = True
        u = p.UniverseOfDiscourse('test_formula_is_mask_similar_to_binary_relation')
        r1a = u.r.declare(2)
        r1b = u.r.declare(2)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        phi1a = u.f(r1a, o1, o2)
        with u.v() as x, u.v() as y:
            phi1b = u.f(r1a, x, y)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x, y}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x, y}))
        with u.v() as x, u.v() as y:
            phi1c = u.f(r1b, x, y)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1c, {x, y}))
            self.assertFalse(phi1c.is_masked_formula_similar_to(phi1a, {x, y}))
        with u.v() as x, u.v() as y, u.v() as z:
            phi1d = u.f(r1b, x, z)
            self.assertFalse(phi1a.is_masked_formula_similar_to(phi1d, {x, y}))
            self.assertFalse(phi1d.is_masked_formula_similar_to(phi1a, {x, y}))

    def test_formula_is_mask_similar_to_embedded(self):
        p.configuration.echo_axiom = True
        u = p.UniverseOfDiscourse('test_formula_is_mask_similar_to_embedded')
        r1a = u.r.declare(2)
        r1b = u.r.declare(2)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        phi1a = u.f(r1a, u.f(r1b, o2, o3), o3)
        with u.v() as x, u.v() as y:
            phi1b = u.f(r1a, u.f(r1b, x, o3), y)
            self.assertTrue(phi1a.is_masked_formula_similar_to(phi1b, {x, y}))
            self.assertTrue(phi1b.is_masked_formula_similar_to(phi1a, {x, y}))
        phi1c = u.f(u.r.land, u.f(r1b, o1, o2), u.f(r1b, o2, o3))
        with u.v() as x1, u.v() as x2, u.v() as x3:
            phi1d = u.f(u.r.land, u.f(r1b, x1, x2), u.f(r1b, x2, x3))
            self.assertTrue(phi1c.is_masked_formula_similar_to(phi1d, {x1, x2, x3}))
            self.assertTrue(phi1d.is_masked_formula_similar_to(phi1c, {x1, x2, x3}))

    def test_formula_is_mask_similar_to_for_modus_ponens(self):
        u = p.UniverseOfDiscourse('test_formula_is_mask_similar_to_for_modus_ponens')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t('modus-ponens-test-theory',
                include_modus_ponens_inference_rule=True)
        t.include_modus_ponens_inference_rule()
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dai(u.f(r1, o2, o3), ap=ap)
        antecedent_statement = t.i.ci.infer_statement(phi1, phi2)
        antecedent = antecedent_statement.valid_proposition

        with u.v() as x, u.v() as y, u.v() as z:
            variable_set = {x, y, z}
            implication = t.dai(
                u.f(
                    u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap)
            antecedent_with_variables = implication.valid_proposition.parameters[0]
            self.assertTrue(antecedent_with_variables.is_masked_formula_similar_to(
                antecedent, variable_set))
            self.assertTrue(antecedent.is_masked_formula_similar_to(
                antecedent_with_variables, variable_set))
