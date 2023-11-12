import unittest
import theory


# from theory.tao_2006_the_peano_axioms import p


class TestTao2006ThePeanoAxioms(unittest.TestCase):
    def test_2_2(self):
        tpa = theory.theory_tao_2006_the_peano_axioms.Tao2006ThePeanoAxioms()
        t = tpa.t
        u = t.u
        plusplus = tpa.plusplus
        phi1 = u.declare_compound_formula(u.c1.is_a, u.declare_compound_formula(plusplus, tpa.zero), tpa.natural_number)
        phi2 = u.declare_compound_formula(u.c1.is_a,
            u.declare_compound_formula(plusplus, u.declare_compound_formula(plusplus, tpa.zero)), tpa.natural_number)
        phi3 = u.declare_compound_formula(u.c1.is_a, u.declare_compound_formula(plusplus,
            u.declare_compound_formula(plusplus, u.declare_compound_formula(plusplus, tpa.zero))), tpa.natural_number)

        self.assertTrue(tpa.proposition_2_2_3.valid_proposition.is_formula_syntactically_equivalent_to(phi1))
        self.assertFalse(tpa.proposition_2_2_3.valid_proposition.is_formula_syntactically_equivalent_to(phi2))
        self.assertFalse(tpa.proposition_2_2_3.valid_proposition.is_formula_syntactically_equivalent_to(phi3))

        self.assertTrue(tpa.p010.valid_proposition.is_formula_syntactically_equivalent_to(phi2))
        self.assertFalse(tpa.p010.valid_proposition.is_formula_syntactically_equivalent_to(phi1))
        self.assertFalse(tpa.p010.valid_proposition.is_formula_syntactically_equivalent_to(phi3))

        self.assertTrue(tpa.p012.valid_proposition.is_formula_syntactically_equivalent_to(phi3))
        self.assertFalse(tpa.p012.valid_proposition.is_formula_syntactically_equivalent_to(phi1))
        self.assertFalse(tpa.p012.valid_proposition.is_formula_syntactically_equivalent_to(phi2))

        phi4 = u.declare_compound_formula(u.c1.is_a, tpa.three, tpa.natural_number)
        self.assertTrue(tpa.proposition_2_1_4.valid_proposition.is_formula_syntactically_equivalent_to(phi4))


if __name__ == '__main__':
    unittest.main()
