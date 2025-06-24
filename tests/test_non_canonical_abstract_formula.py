import pytest

import punctilious as pu


class TestNonCanonicalAbstractFormula:
    def test_construction_success(self):
        phi1 = pu.afl.NonCanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 2, 3,))
        phi2 = pu.afl.NonCanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 0, 0,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.NonCanonicalAbstractFormula(t=(((),), (),), s=(0, 2,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.NonCanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 0, 2, 0,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.NonCanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 0, 1, 0, 3, 7, 1))

    def test_iterate_immediate_sub_sequences(self, s0, s1, s2, s3, s4, s5, s00, s01, ncaf1, rgfs0, ncaf2a, rgfs01,
                                             ncaf6a,
                                             rgfs012345,
                                             ncaf12a, rgfs0123456789_10_11):
        l = tuple(t for t in ncaf1.iterate_immediate_sub_sequences())
        assert len(l) == 0
        l = tuple(t for t in ncaf2a.iterate_immediate_sub_sequences())
        assert l[0] == s0
        l = tuple(t for t in ncaf6a.iterate_immediate_sub_sequences())
        assert l[0] == s1
        assert l[1] == s2
        assert l[2] == s3
        assert l[3] == s4
        assert l[4] == s5
        l = tuple(t for t in ncaf12a.iterate_immediate_sub_sequences())
        assert l[0] == s1
        assert l[1] == (2, 3,)
        assert l[2] == (4, 5, 6, 7, 8, 9,)
        assert l[3] == (10, 11,)

    def test_iterate_immediate_sub_natural_numbers_sequences(self, ncaf1, rgfs0, ncaf2a, rgfs01, ncaf6a,
                                                             rgfs012345,
                                                             ncaf12a, rgfs0123456789_10_11):
        l = tuple(t for t in ncaf1.iterate_immediate_sub_restricted_growth_function_sequences())
        assert len(l) == 0
        l = tuple(t for t in ncaf2a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgfs0
        l = tuple(t for t in ncaf6a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgfs0
        assert l[1] == rgfs0
        assert l[2] == rgfs0
        assert l[3] == rgfs0
        assert l[4] == rgfs0
        l = tuple(t for t in ncaf12a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgfs0
        assert l[1] == rgfs01
        assert l[2] == rgfs012345
        assert l[3] == rgfs01

    def test_iterate_sub_natural_numbers_sequences(self, ncaf1, rgfs0, ncaf2a, rgfs01, ncaf6a, ncaf12a,
                                                   rgfs012345):
        l = tuple(t for t in ncaf1.iterate_sub_natural_numbers_sequences())
        assert l[0] == ncaf1.restricted_growth_function_sequence
        l = tuple(t for t in ncaf2a.iterate_sub_natural_numbers_sequences())
        assert l[0] == ncaf2a.restricted_growth_function_sequence
        assert l[1] == rgfs0
        l = tuple(t for t in ncaf6a.iterate_sub_natural_numbers_sequences())
        assert l[0] == ncaf6a.restricted_growth_function_sequence
        assert l[1] == rgfs0
        assert l[2] == rgfs0
        assert l[3] == rgfs0
        assert l[4] == rgfs0
        assert l[5] == rgfs0
        l = tuple(t for t in ncaf12a.iterate_sub_natural_numbers_sequences())
        assert l[0] == ncaf12a.restricted_growth_function_sequence
        assert l[1] == rgfs0
        assert l[2] == rgfs01
        assert l[3] == rgfs0
        assert l[4] == rgfs012345
        assert l[5] == rgfs0
        assert l[6] == rgfs0
        assert l[7] == rgfs0
        assert l[8] == rgfs0
        assert l[9] == rgfs0
        assert l[10] == rgfs01
        assert l[11] == rgfs0

    def test_iterate_sub_formulas_direct(self, ncaf1, ncaf2a, ncaf2b, ncaf12a, ncaf6a):
        l = tuple(af for af in ncaf1.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(af for af in ncaf2a.iterate_immediate_sub_formulas())
        assert l[0] == ncaf1
        l = tuple(af for af in ncaf2b.iterate_immediate_sub_formulas())
        assert l[0] == ncaf1
        l = tuple(af for af in ncaf12a.iterate_immediate_sub_formulas())
        assert l[0] == ncaf1
        assert l[1] == ncaf2b
        assert l[2] == ncaf6a
        assert l[3] == ncaf2b

    def test_iterate_sub_formulas_depth_first_ascending(self, ncaf1, ncaf2a, ncaf2b, ncaf6a, ncaf12a):
        l = tuple(t for t in ncaf1.iterate_sub_formulas())
        assert l[0] == ncaf1
        l = tuple(t for t in ncaf2a.iterate_sub_formulas())
        assert l[0] == ncaf2a
        assert l[1] == ncaf1
        l = tuple(t for t in ncaf2b.iterate_sub_formulas())
        assert l[0] == ncaf2b
        assert l[1] == ncaf1
        l = tuple(t for t in ncaf6a.iterate_sub_formulas())
        assert l[0] == ncaf6a
        assert l[1] == ncaf1
        assert l[2] == ncaf1
        assert l[3] == ncaf1
        assert l[4] == ncaf1
        assert l[5] == ncaf1
        l = tuple(t for t in ncaf12a.iterate_sub_formulas())
        assert l[0] == ncaf12a
        assert l[1] == ncaf1
        assert l[2] == ncaf2b
        assert l[3] == ncaf1
        assert l[4] == ncaf6a
        assert l[5] == ncaf1
        assert l[6] == ncaf1
        assert l[7] == ncaf1
        assert l[8] == ncaf1
        assert l[9] == ncaf1
        assert l[10] == ncaf2b
        assert l[11] == ncaf1

    def test_main_sequence_element(self, ncaf1, ncaf2a, ncaf2b, ncaf6a, ncaf12a):
        assert ncaf1.main_sequence_element == 0
        assert ncaf2a.main_sequence_element == 0
        assert ncaf2b.main_sequence_element == 0
        assert ncaf6a.main_sequence_element == 0
        assert ncaf12a.main_sequence_element == 0

    def test_tree_size(self, ncaf1, ncaf2a, ncaf2b, ncaf6a, ncaf12a):
        assert ncaf1.tree_size == 1
        assert ncaf2a.tree_size == 2
        assert ncaf2b.tree_size == 2
        assert ncaf6a.tree_size == 6
        assert ncaf12a.tree_size == 12

    def test_formula_degree(self, ncaf1, ncaf2a, ncaf2b, ncaf6a, ncaf12a):
        assert ncaf1.formula_degree == 0
        assert ncaf2a.formula_degree == 1
        assert ncaf2b.formula_degree == 1
        assert ncaf6a.formula_degree == 1
        assert ncaf12a.formula_degree == 4

    def test_is_abstract_formula_equivalent_to(self, ncaf1, ncaf2a, ncaf2b, ncaf6a, ncaf12a):
        assert ncaf1.is_canonical_abstract_formula_equivalent_to(caf1)
        assert ncaf2a.is_canonical_abstract_formula_equivalent_to(caf2a)
        assert ncaf2b.is_canonical_abstract_formula_equivalent_to(caf2b)
        assert ncaf6a.is_canonical_abstract_formula_equivalent_to(caf6a)
        assert ncaf12a.is_canonical_abstract_formula_equivalent_to(caf12a)

        assert not ncaf1.is_canonical_abstract_formula_equivalent_to(caf2a)
        assert not ncaf1.is_canonical_abstract_formula_equivalent_to(caf2b)
        assert not ncaf1.is_canonical_abstract_formula_equivalent_to(caf6a)
        assert not ncaf1.is_canonical_abstract_formula_equivalent_to(caf12a)

    def test_extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(self):
        tree_of_pairs = (0, (),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == ((), (0,),)
        tree_of_pairs = (3, ((2, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((),), (3, 2,),)
        tree_of_pairs = (3, ((9, (),), (8, (),), (7, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((), (), (),), (3, 9, 8, 7,),)
        tree_of_pairs = (3, ((9, (),), (8, ((3, ((2, ((3, ((2, (),),),),),),),),),), (7, ((0, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((), (((((),),),),), ((),),), (3, 9, 8, 3, 2, 3, 2, 7, 0,),)

    def test_build_formula_from_tree_of_integer_tuple_pairs(self, ncaf1):
        tree_of_pairs = (0, (),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.NonCanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((0, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.NonCanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_non_canonical_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.NonCanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_non_canonical_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (2, (),), (3, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.NonCanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_non_canonical_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (0, ((1, ((2, ((3, ((1, (),),),),),),),),),), (4, ((1, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.NonCanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_non_canonical_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi

    def test_get_sub_tree_by_path(self, ncaf1, ncaf2a, ncaf6a, ncaf12a, ncaf_big):
        assert ncaf1.get_sub_formula_by_path((0,)) == ncaf1
        assert ncaf2a.get_sub_formula_by_path((0,)) == ncaf2a
        assert ncaf2a.get_sub_formula_by_path((0, 0,)) == ncaf1

        assert ncaf_big.get_sub_formula_by_path((0, 3,)) == ncaf12a
        assert ncaf_big.get_sub_formula_by_path((0, 3, 2,)) == (0, 1, 2,)
        assert ncaf_big.get_sub_formula_by_path((0, 3, 2, 4,)) == (0, 1, 2,)
