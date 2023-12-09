from unittest import TestCase
import punctilious as pu


class TestHypothesis(TestCase):
    def test_hypothesis(self):
        import sample.sample_hypothesis as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        f: pu.Connective = test.f
        h: pu.Hypothesis = test.h
        self.assertTrue(h.child_statement.is_formula_syntactically_equivalent_to(phi=f(o1, o2)))
        self.assertTrue(h.child_theory.contains_statement_in_theory_chain(phi=test.predecessor))
        successor: pu.InferredStatement = test.successor
        self.assertFalse(h.child_theory.contains_statement_in_theory_chain(phi=successor))
