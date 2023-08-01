import unittest
import theories.tao_2006_the_peano_axioms as tpa

# from theories.tao_2006_the_peano_axioms import p

u = tpa.u
t = tpa.t


class TestTao2006ThePeanoAxioms(unittest.TestCase):
    def test_2_2(self):
        phi1 = u.f(tpa.is_a, u.f(tpa.plusplus, tpa.zero), tpa.natural_number)
        phi2 = u.f(tpa.is_a, u.f(tpa.plusplus, u.f(tpa.plusplus, tpa.zero)), tpa.natural_number)
        phi3 = u.f(
            tpa.is_a, u.f(tpa.plusplus, u.f(tpa.plusplus, u.f(tpa.plusplus, tpa.zero))),
            tpa.natural_number)

        self.assertTrue(
            tpa.p004.valid_proposition.is_formula_equivalent_to(phi1))
        self.assertFalse(
            tpa.p004.valid_proposition.is_formula_equivalent_to(phi2))
        self.assertFalse(
            tpa.p004.valid_proposition.is_formula_equivalent_to(phi3))

        self.assertTrue(
            tpa.p010.valid_proposition.is_formula_equivalent_to(phi2))
        self.assertFalse(
            tpa.p010.valid_proposition.is_formula_equivalent_to(phi1))
        self.assertFalse(
            tpa.p010.valid_proposition.is_formula_equivalent_to(phi3))

        self.assertTrue(
            tpa.p012.valid_proposition.is_formula_equivalent_to(
                phi3))
        self.assertFalse(
            tpa.p012.valid_proposition.is_formula_equivalent_to(
                phi1))
        self.assertFalse(
            tpa.p012.valid_proposition.is_formula_equivalent_to(
                phi2))

        phi4 = u.f(tpa.is_a, tpa.three, tpa.natural_number)
        self.assertTrue(
            tpa.p022.valid_proposition.is_formula_equivalent_to(phi4))


if __name__ == '__main__':
    unittest.main()
