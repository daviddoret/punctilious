import unittest
import core as pt
import theories.tao_2006_the_peano_axioms as tpa

u = tpa.u
t = tpa.t


class TestTao2006ThePeanoAxioms(unittest.TestCase):
    def test_2_2(self):
        phi1 = u.f(tpa.is_a, u.f(tpa.suc, tpa.zero), tpa.nat)
        phi2 = u.f(tpa.is_a, u.f(tpa.suc, u.f(tpa.suc, tpa.zero)), tpa.nat)
        phi3 = u.f(
            tpa.is_a, u.f(tpa.suc, u.f(tpa.suc, u.f(tpa.suc, tpa.zero))),
            tpa.nat)

        self.assertTrue(
            tpa.p_2_2_3.valid_proposition.is_formula_equivalent_to(phi1))
        self.assertFalse(
            tpa.p_2_2_3.valid_proposition.is_formula_equivalent_to(phi2))
        self.assertFalse(
            tpa.p_2_2_3.valid_proposition.is_formula_equivalent_to(phi3))

        self.assertTrue(
            tpa.p_2_2_4.valid_proposition.is_formula_equivalent_to(phi2))
        self.assertFalse(
            tpa.p_2_2_4.valid_proposition.is_formula_equivalent_to(phi1))
        self.assertFalse(
            tpa.p_2_2_4.valid_proposition.is_formula_equivalent_to(phi3))

        self.assertTrue(
            tpa.proposition_2_2_5.valid_proposition.is_formula_equivalent_to(
                phi3))
        self.assertFalse(
            tpa.proposition_2_2_5.valid_proposition.is_formula_equivalent_to(
                phi1))
        self.assertFalse(
            tpa.proposition_2_2_5.valid_proposition.is_formula_equivalent_to(
                phi2))

        phi4 = u.f(tpa.is_a, tpa.three, tpa.nat)
        self.assertTrue(
            tpa.p_2_1_4.valid_proposition.is_formula_equivalent_to(phi4))


if __name__ == '__main__':
    unittest.main()
