from unittest import TestCase
import punctilious as pu


class TestHypothesis(TestCase):
    def test_hypothesis(self):
        import sample.sample_hypothesis as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        f: pu.Relation = test.f
        h: pu.Hypothesis = test.h
        self.assertTrue(h.child_statement.is_formula_syntactically_equivalent_to(o2=f(o1, o2)))
        self.assertTrue(h.child_theory.contains_theoretical_objct(test.predecessor))
        self.assertFalse(h.child_theory.contains_theoretical_objct(test.successor))
