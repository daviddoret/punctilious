import unittest
import theory as tpa


# from theory.tao_2006_the_peano_axioms import p


class TestTao2006ThePeanoAxioms(unittest.TestCase):
    def test_2_2(self):
        t = tpa.Tao2006ThePeanoAxioms().develop()
        u = t.u
        phi1 = u.f(u.r.is_a, u.f(tpa.plusplus, u.r.zero), u.r.natural_number)
        phi2 = u.f(u.r.is_a, u.f(tpa.plusplus, u.f(tpa.plusplus, u.r.zero)), u.r.natural_number)
        phi3 = u.f(u.r.is_a, u.f(tpa.plusplus, u.f(tpa.plusplus, u.f(tpa.plusplus, u.r.zero))),
            u.r.natural_number)

        self.assertTrue(t.p004.valid_proposition.is_formula_syntactically_equivalent_to(phi1))
        self.assertFalse(tpa.p004.valid_proposition.is_formula_syntactically_equivalent_to(phi2))
        self.assertFalse(tpa.p004.valid_proposition.is_formula_syntactically_equivalent_to(phi3))

        self.assertTrue(tpa.p010.valid_proposition.is_formula_syntactically_equivalent_to(phi2))
        self.assertFalse(tpa.p010.valid_proposition.is_formula_syntactically_equivalent_to(phi1))
        self.assertFalse(tpa.p010.valid_proposition.is_formula_syntactically_equivalent_to(phi3))

        self.assertTrue(tpa.p012.valid_proposition.is_formula_syntactically_equivalent_to(phi3))
        self.assertFalse(tpa.p012.valid_proposition.is_formula_syntactically_equivalent_to(phi1))
        self.assertFalse(tpa.p012.valid_proposition.is_formula_syntactically_equivalent_to(phi2))

        phi4 = u.f(u.r.is_a, tpa.three, u.r.natural_number)
        self.assertTrue(tpa.p022.valid_proposition.is_formula_syntactically_equivalent_to(phi4))


if __name__ == '__main__':
    unittest.main()
