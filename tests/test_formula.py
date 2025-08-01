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
        assert l[0] == pu.cc.one
        l = tuple(t for t in phi2a.iterate_connectives())
        assert l[0] == pu.cc.one
        assert l[1] == pu.cc.one
        l = tuple(t for t in phi2b.iterate_connectives())
        assert l[0] == pu.cc.minus
        assert l[1] == pu.cc.one
        l = tuple(t for t in phi6a.iterate_connectives())
        assert l[0] == pu.cc.set_by_extension
        assert l[1] == pu.cc.one
        assert l[2] == pu.cc.two
        assert l[3] == pu.cc.three
        assert l[4] == pu.cc.four
        assert l[5] == pu.cc.five

    def test_main_connective(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.main_connective == pu.cc.one
        assert phi2a.main_connective == pu.cc.one
        assert phi2b.main_connective == pu.cc.minus
        assert phi6a.main_connective == pu.cc.set_by_extension

    def test_iterate_immediate_sub_formulas(self, lrpt1, phi1a, phi2a, phi2b, phi6a):
        l = tuple(t for t in phi1a.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(t for t in phi2a.iterate_immediate_sub_formulas())
        assert l[0] == phi1a
        l = tuple(t for t in phi2b.iterate_immediate_sub_formulas())
        assert l[0] == phi1a
        l = tuple(t for t in phi6a.iterate_immediate_sub_formulas())
        assert l[0] == pu.fl.Formula(t=lrpt1, s=(pu.cc.one,))
        assert l[1] == pu.fl.Formula(t=lrpt1, s=(pu.cc.two,))
        assert l[2] == pu.fl.Formula(t=lrpt1, s=(pu.cc.three,))
        assert l[3] == pu.fl.Formula(t=lrpt1, s=(pu.cc.four,))
        assert l[4] == pu.fl.Formula(t=lrpt1, s=(pu.cc.five,))

    def test_is_immediate_sub_formula_of(self, lrpt1, phi1a, phi2a, phi2b, phi6a):
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.one,)).is_immediate_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.two,)).is_immediate_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.three,)).is_immediate_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.four,)).is_immediate_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.five,)).is_immediate_sub_formula_of(phi6a)

    def test_is_sub_formula_of(self, lrpt1, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.is_sub_formula_of(phi1a)
        assert phi2a.is_sub_formula_of(phi2a)
        assert phi2b.is_sub_formula_of(phi2b)
        assert phi6a.is_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.one,)).is_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.two,)).is_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.three,)).is_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.four,)).is_sub_formula_of(phi6a)
        assert pu.fl.Formula(t=lrpt1, s=(pu.cc.five,)).is_sub_formula_of(phi6a)

    def test_iterate_sub_formulas(self, lrpt1, phi1a, phi2a, phi2b, phi6a):
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
        assert l[1] == pu.fl.Formula(t=lrpt1, s=(pu.cc.one,))
        assert l[2] == pu.fl.Formula(t=lrpt1, s=(pu.cc.two,))
        assert l[3] == pu.fl.Formula(t=lrpt1, s=(pu.cc.three,))
        assert l[4] == pu.fl.Formula(t=lrpt1, s=(pu.cc.four,))
        assert l[5] == pu.fl.Formula(t=lrpt1, s=(pu.cc.five,))

    def test_is_formula_equivalent_to(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.is_formula_equivalent_to(phi1a)
        assert phi2a.is_formula_equivalent_to(phi2a)
        assert phi2b.is_formula_equivalent_to(phi2b)
        assert phi6a.is_formula_equivalent_to(phi6a)

        assert not phi1a.is_formula_equivalent_to(phi2a)
        assert not phi1a.is_formula_equivalent_to(phi2b)
        assert not phi1a.is_formula_equivalent_to(phi6a)

    def test_is_increasing(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.is_increasing
        assert phi2a.is_increasing
        assert phi2b.is_increasing
        assert not phi6a.is_increasing

    def test_is_strictly_increasing(self, phi1a, phi2a, phi2b, phi6a):
        assert phi1a.is_strictly_increasing
        assert phi2a.is_strictly_increasing
        assert phi2b.is_strictly_increasing
        assert not phi6a.is_strictly_increasing
