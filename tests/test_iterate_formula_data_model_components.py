from unittest import TestCase
import punctilious as pu


class TestIterateFormulaDataModelComponents(TestCase):
    def test_iterate_formula_data_model_components(self):
        import sample.sample_iterate_formula_data_model_components as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        x1: pu.FreeVariable = test.x
        y1: pu.Connective = test.y
        phi1: pu.CompoundFormula = test.phi1

        expected1: tuple = (o1,)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected1, psi=test.output1)))

        expected2: tuple = (phi1, r1, o1, o2)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected2, psi=test.output2)))

        rho1: pu.Formula
        _, rho1, _ = pu.verify_formula(u=u, input_value=r2(o3, r1(o1, o2)))
        expected3: tuple = (rho1, r2, o3, phi1, r1, o1, o2)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected3, psi=test.output3)))

        expected4: tuple = (r2, r1)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected4, psi=test.output4)))

        expected5: tuple = (r1, r2, r2, r1, y1, r2, x1, r1, r2, r1, r1, y1)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected5, psi=test.output5)))

        expected6: tuple = (y1, x1, y1)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected6, psi=test.output6)))

        expected7: tuple = (r1,)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected7, psi=test.output7)))

        expected8: tuple = (r1,)
        self.assertTrue(
            all(pu.is_alpha_equivalent_to_iterable(u=u, phi=expected8, psi=test.output8)))
