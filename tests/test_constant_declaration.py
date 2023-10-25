from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestConstantDeclaration(TestCase):

    def test_ci(self):
        import sample.sample_constant as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        # x: pu.Variable = test.x
        # y: pu.Variable = test.y
        c1: pu.ConstantDeclaration = test.c1
        c2: pu.ConstantDeclaration = test.c2
        c3: pu.ConstantDeclaration = test.c3

        self.assertTrue(c1.value.is_formula_syntactically_equivalent_to(phi=o1))
        self.assertEqual('c1', c1.rep_formula(pu.encodings.plaintext))
        self.assertEqual('o1', c1.value.rep_formula(pu.encodings.plaintext))
        self.assertTrue(c2.value.is_formula_syntactically_equivalent_to(phi=o2 | r1 | o3))
        self.assertEqual('c2', c2.rep_formula(pu.encodings.plaintext))
        self.assertEqual('r1(o2, o3)', c2.value.rep_formula(pu.encodings.plaintext))
        with u.with_variable(symbol='x') as x, u.with_variable('y') as y:
            self.assertTrue(c3.value.is_alpha_equivalent_to(phi=x | r1 | y))
            self.assertEqual('c3', c3.rep_formula(pu.encodings.plaintext))
            self.assertEqual('r1(x1, y1)', c3.value.rep_formula(pu.encodings.plaintext))
