import pytest

import punctilious as pu


class TestAbstractFormula:
    def test_construction_success(self):
        phi1 = pu.af.AbstractFormula(t=(((),), (),), s=(0, 1, 2, 3,))
        phi2 = pu.af.AbstractFormula(t=(((),), (),), s=(0, 1, 0, 0,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.af.AbstractFormula(t=(((),), (),), s=(0, 2, 1, 0,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.af.AbstractFormula(t=(((),), (),), s=(0, 1, 0,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.af.AbstractFormula(t=(((),), (),), s=(0, 1, 0, 1, 0,))

    def test_iterate_immediate_sub_sequences(self, s1a, s1b, s1c, s1d, s1e, s1f, s2a, s2b, af1, rgf1, af2a, rgf2b, af6a,
                                             rgf6a,
                                             af12a, rgf12a):
        l = tuple(t for t in af1.iterate_immediate_sub_sequences())
        assert len(l) == 0
        l = tuple(t for t in af2a.iterate_immediate_sub_sequences())
        assert l[0] == s1a
        l = tuple(t for t in af6a.iterate_immediate_sub_sequences())
        assert l[0] == s1b
        assert l[1] == s1c
        assert l[2] == s1d
        assert l[3] == s1e
        assert l[4] == s1f
        l = tuple(t for t in af12a.iterate_immediate_sub_sequences())
        assert l[0] == s1b
        assert l[1] == (2, 3,)
        assert l[2] == (4, 5, 6, 7, 8, 9,)
        assert l[3] == (10, 11,)

    def test_iterate_immediate_sub_restricted_growth_function_sequences(self, af1, rgf1, af2a, rgf2b, af6a, rgf6a,
                                                                        af12a, rgf12a):
        l = tuple(t for t in af1.iterate_immediate_sub_restricted_growth_function_sequences())
        assert len(l) == 0
        l = tuple(t for t in af2a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgf1
        l = tuple(t for t in af6a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgf1
        assert l[1] == rgf1
        assert l[2] == rgf1
        assert l[3] == rgf1
        assert l[4] == rgf1
        l = tuple(t for t in af12a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgf1
        assert l[1] == rgf2b
        assert l[2] == rgf6a
        assert l[3] == rgf2b

    def test_iterate_sub_restricted_growth_function_sequences(self, af1, rgf1, af2a, rgf2b, af6a, af12a, rgf6a):
        l = tuple(t for t in af1.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == af1.restricted_growth_function_sequence
        l = tuple(t for t in af2a.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == af2a.restricted_growth_function_sequence
        assert l[1] == rgf1
        l = tuple(t for t in af6a.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == af6a.restricted_growth_function_sequence
        assert l[1] == rgf1
        assert l[2] == rgf1
        assert l[3] == rgf1
        assert l[4] == rgf1
        assert l[5] == rgf1
        l = tuple(t for t in af12a.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == af12a.restricted_growth_function_sequence
        assert l[1] == rgf1
        assert l[2] == rgf2b
        assert l[3] == rgf1
        assert l[4] == rgf6a
        assert l[5] == rgf1
        assert l[6] == rgf1
        assert l[7] == rgf1
        assert l[8] == rgf1
        assert l[9] == rgf1
        assert l[10] == rgf2b
        assert l[11] == rgf1

    def test_iterate_sub_formulas_direct(self, af1, af2a, af2b, af12a, af6a):
        l = tuple(af for af in af1.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(af for af in af2a.iterate_immediate_sub_formulas())
        assert l[0] == af1
        l = tuple(af for af in af2b.iterate_immediate_sub_formulas())
        assert l[0] == af1
        l = tuple(af for af in af12a.iterate_immediate_sub_formulas())
        assert l[0] == af1
        assert l[1] == af2b
        assert l[2] == af6a
        assert l[3] == af2b

    def test_iterate_sub_formulas_depth_first_ascending(self, af1, af2a, af2b, af6a, af12a):
        l = tuple(t for t in af1.iterate_sub_formulas())
        assert l[0] == af1
        l = tuple(t for t in af2a.iterate_sub_formulas())
        assert l[0] == af2a
        assert l[1] == af1
        l = tuple(t for t in af2b.iterate_sub_formulas())
        assert l[0] == af2b
        assert l[1] == af1
        l = tuple(t for t in af6a.iterate_sub_formulas())
        assert l[0] == af6a
        assert l[1] == af1
        assert l[2] == af1
        assert l[3] == af1
        assert l[4] == af1
        assert l[5] == af1
        l = tuple(t for t in af12a.iterate_sub_formulas())
        assert l[0] == af12a
        assert l[1] == af1
        assert l[2] == af2b
        assert l[3] == af1
        assert l[4] == af6a
        assert l[5] == af1
        assert l[6] == af1
        assert l[7] == af1
        assert l[8] == af1
        assert l[9] == af1
        assert l[10] == af2b
        assert l[11] == af1

    def test_main_sequence_element(self, af1, af2a, af2b, af6a, af12a):
        assert af1.main_sequence_element == 0
        assert af2a.main_sequence_element == 0
        assert af2b.main_sequence_element == 0
        assert af6a.main_sequence_element == 0
        assert af12a.main_sequence_element == 0

    def test_tree_size(self, af1, af2a, af2b, af6a, af12a):
        assert af1.tree_size == 1
        assert af2a.tree_size == 2
        assert af2b.tree_size == 2
        assert af6a.tree_size == 6
        assert af12a.tree_size == 12

    def test_formula_degree(self, af1, af2a, af2b, af6a, af12a):
        assert af1.formula_degree == 0
        assert af2a.formula_degree == 1
        assert af2b.formula_degree == 1
        assert af6a.formula_degree == 1
        assert af12a.formula_degree == 4

    def test_is_abstract_formula_equivalent_to(self, af1, af2a, af2b, af6a, af12a):
        assert af1.is_abstract_formula_equivalent_to(af1)
        assert af2a.is_abstract_formula_equivalent_to(af2a)
        assert af2b.is_abstract_formula_equivalent_to(af2b)
        assert af6a.is_abstract_formula_equivalent_to(af6a)
        assert af12a.is_abstract_formula_equivalent_to(af12a)

        assert not af1.is_abstract_formula_equivalent_to(af2a)
        assert not af1.is_abstract_formula_equivalent_to(af2b)
        assert not af1.is_abstract_formula_equivalent_to(af6a)
        assert not af1.is_abstract_formula_equivalent_to(af12a)
