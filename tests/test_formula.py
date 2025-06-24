import punctilious as pu


# import pytest


class TestFormula:
    def test_tree_size(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.tree_size == 1
        assert phi2a.tree_size == 2
        assert phi2b.tree_size == 2
        assert phi6a.tree_size == 6

    def test_iterate_connectives(self, phi1a, phi2a, phi2b, phi6a):
        l = tuple(t for t in phi1a.iterate_connectives())
        assert l[0] == pu.connective_library.one
        l = tuple(t for t in phi2a.iterate_connectives())
        assert l[0] == pu.connective_library.one
        assert l[1] == pu.connective_library.one
        l = tuple(t for t in phi2b.iterate_connectives())
        assert l[0] == pu.connective_library.minus
        assert l[1] == pu.connective_library.one
        l = tuple(t for t in phi6a.iterate_connectives())
        assert l[0] == pu.connective_library.set_by_extension
        assert l[1] == pu.connective_library.one
        assert l[2] == pu.connective_library.two
        assert l[3] == pu.connective_library.three
        assert l[4] == pu.connective_library.four
        assert l[5] == pu.connective_library.five

    def test_main_connective(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.main_connective == pu.connective_library.one
        assert phi2a.main_connective == pu.connective_library.one
        assert phi2b.main_connective == pu.connective_library.minus
        assert phi6a.main_connective == pu.connective_library.set_by_extension

    def test_iterate_immediate_sub_formulas(self, caf1, phi1a, phi2a, phi2b, phi6a):
        l = tuple(t for t in phi1a.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(t for t in phi2a.iterate_immediate_sub_formulas())
        assert l[0] == phi1a
        l = tuple(t for t in phi2b.iterate_immediate_sub_formulas())
        assert l[0] == phi1a
        l = tuple(t for t in phi6a.iterate_immediate_sub_formulas())
        assert l[0] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.one,))
        assert l[1] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.two,))
        assert l[2] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.three,))
        assert l[3] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.four,))
        assert l[4] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.five,))

    def test_is_immediate_sub_formula_of(self, caf1, phi1a, phi2a, phi2b, phi6a):
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.one,)).is_immediate_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.two,)).is_immediate_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.three,)).is_immediate_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.four,)).is_immediate_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.five,)).is_immediate_sub_formula_of(phi6a)

    def test_is_sub_formula_of(self, caf1, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.is_sub_formula_of(phi1a)
        assert phi2a.is_sub_formula_of(phi2a)
        assert phi2b.is_sub_formula_of(phi2b)
        assert phi6a.is_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.one,)).is_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.two,)).is_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.three,)).is_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.four,)).is_sub_formula_of(phi6a)
        assert pu.formula.Formula(phi=caf1, s=(pu.connective_library.five,)).is_sub_formula_of(phi6a)

    def test_iterate_sub_formulas(self, caf1, phi1a, phi2a, phi2b, phi6a):
        l = tuple(t for t in phi1a.iterate_sub_formulas())
        assert l[0] == phi1a
        l = tuple(t for t in phi2a.iterate_sub_formulas())
        assert l[0] == phi2a
        assert l[1] == phi1a
        l = tuple(t for t in phi2b.iterate_sub_formulas())
        assert l[0] == phi2b
        assert l[1] == phi1a
        l = tuple(t for t in phi6a.iterate_sub_formulas())
        assert l[0] == phi6a
        assert l[1] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.one,))
        assert l[2] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.two,))
        assert l[3] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.three,))
        assert l[4] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.four,))
        assert l[5] == pu.formula.Formula(phi=caf1, s=(pu.connective_library.five,))

    def test_is_formula_equivalent_to(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.is_formula_equivalent_to(phi1a)
        assert phi2a.is_formula_equivalent_to(phi2a)
        assert phi2b.is_formula_equivalent_to(phi2b)
        assert phi6a.is_formula_equivalent_to(phi6a)

        assert not phi1a.is_formula_equivalent_to(phi2a)
        assert not phi1a.is_formula_equivalent_to(phi2b)
        assert not phi1a.is_formula_equivalent_to(phi6a)
