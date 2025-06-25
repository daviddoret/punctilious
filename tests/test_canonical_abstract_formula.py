import pytest

import punctilious as pu


class TestAbstractFormula:
    def test_construction_success(self):
        phi1 = pu.afl.CanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 2, 3,))
        phi2 = pu.afl.CanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 0, 0,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.CanonicalAbstractFormula(t=(((),), (),), s=(0, 2, 1, 0,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.CanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 0,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.CanonicalAbstractFormula(t=(((),), (),), s=(0, 1, 0, 1, 0,))

    def test_iterate_immediate_sub_sequences(self, s0, s1, s2, s3, s4, s5, s00, s01, caf1, rgfs0, caf2a, rgfs01, caf6a,
                                             rgfs012345,
                                             caf12a, rgfs0123456789_10_11):
        l = tuple(t for t in caf1.iterate_immediate_sub_sequences())
        assert len(l) == 0
        l = tuple(t for t in caf2a.iterate_immediate_sub_sequences())
        assert l[0] == s0
        l = tuple(t for t in caf6a.iterate_immediate_sub_sequences())
        assert l[0] == s1
        assert l[1] == s2
        assert l[2] == s3
        assert l[3] == s4
        assert l[4] == s5
        l = tuple(t for t in caf12a.iterate_immediate_sub_sequences())
        assert l[0] == s1
        assert l[1] == (2, 3,)
        assert l[2] == (4, 5, 6, 7, 8, 9,)
        assert l[3] == (10, 11,)

    def test_iterate_immediate_sub_restricted_growth_function_sequences(self, caf1, rgfs0, caf2a, rgfs01, caf6a,
                                                                        rgfs012345,
                                                                        caf12a, rgfs0123456789_10_11):
        l = tuple(t for t in caf1.iterate_immediate_sub_restricted_growth_function_sequences())
        assert len(l) == 0
        l = tuple(t for t in caf2a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgfs0
        l = tuple(t for t in caf6a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgfs0
        assert l[1] == rgfs0
        assert l[2] == rgfs0
        assert l[3] == rgfs0
        assert l[4] == rgfs0
        l = tuple(t for t in caf12a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == rgfs0
        assert l[1] == rgfs01
        assert l[2] == rgfs012345
        assert l[3] == rgfs01

    def test_iterate_sub_restricted_growth_function_sequences(self, caf1, rgfs0, caf2a, rgfs01, caf6a, caf12a,
                                                              rgfs012345):
        l = tuple(t for t in caf1.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == caf1.restricted_growth_function_sequence
        l = tuple(t for t in caf2a.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == caf2a.restricted_growth_function_sequence
        assert l[1] == rgfs0
        l = tuple(t for t in caf6a.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == caf6a.restricted_growth_function_sequence
        assert l[1] == rgfs0
        assert l[2] == rgfs0
        assert l[3] == rgfs0
        assert l[4] == rgfs0
        assert l[5] == rgfs0
        l = tuple(t for t in caf12a.iterate_sub_restricted_growth_function_sequences())
        assert l[0] == caf12a.restricted_growth_function_sequence
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

    def test_iterate_sub_formulas_direct(self, caf1, caf2a, caf2b, caf12a, caf6a):
        l = tuple(af for af in caf1.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(af for af in caf2a.iterate_immediate_sub_formulas())
        assert l[0] == caf1
        l = tuple(af for af in caf2b.iterate_immediate_sub_formulas())
        assert l[0] == caf1
        l = tuple(af for af in caf12a.iterate_immediate_sub_formulas())
        assert l[0] == caf1
        assert l[1] == caf2b
        assert l[2] == caf6a
        assert l[3] == caf2b

    def test_iterate_sub_formulas_depth_first_ascending(self, caf1, caf2a, caf2b, caf6a, caf12a):
        l = tuple(t for t in caf1.iterate_sub_formulas())
        assert l[0] == caf1
        l = tuple(t for t in caf2a.iterate_sub_formulas())
        assert l[0] == caf2a
        assert l[1] == caf1
        l = tuple(t for t in caf2b.iterate_sub_formulas())
        assert l[0] == caf2b
        assert l[1] == caf1
        l = tuple(t for t in caf6a.iterate_sub_formulas())
        assert l[0] == caf6a
        assert l[1] == caf1
        assert l[2] == caf1
        assert l[3] == caf1
        assert l[4] == caf1
        assert l[5] == caf1
        l = tuple(t for t in caf12a.iterate_sub_formulas())
        assert l[0] == caf12a
        assert l[1] == caf1
        assert l[2] == caf2b
        assert l[3] == caf1
        assert l[4] == caf6a
        assert l[5] == caf1
        assert l[6] == caf1
        assert l[7] == caf1
        assert l[8] == caf1
        assert l[9] == caf1
        assert l[10] == caf2b
        assert l[11] == caf1

    def test_main_sequence_element(self, caf1, caf2a, caf2b, caf6a, caf12a):
        assert caf1.main_element == 0
        assert caf2a.main_element == 0
        assert caf2b.main_element == 0
        assert caf6a.main_element == 0
        assert caf12a.main_element == 0

    def test_tree_size(self, caf1, caf2a, caf2b, caf6a, caf12a):
        assert caf1.tree_size == 1
        assert caf2a.tree_size == 2
        assert caf2b.tree_size == 2
        assert caf6a.tree_size == 6
        assert caf12a.tree_size == 12

    def test_formula_degree(self, caf1, caf2a, caf2b, caf6a, caf12a):
        assert caf1.formula_degree == 0
        assert caf2a.formula_degree == 1
        assert caf2b.formula_degree == 1
        assert caf6a.formula_degree == 1
        assert caf12a.formula_degree == 4

    def test_is_abstract_formula_equivalent_to(self, caf1, caf2a, caf2b, caf6a, caf12a):
        assert caf1.is_canonical_abstract_formula_equivalent_to(caf1)
        assert caf2a.is_canonical_abstract_formula_equivalent_to(caf2a)
        assert caf2b.is_canonical_abstract_formula_equivalent_to(caf2b)
        assert caf6a.is_canonical_abstract_formula_equivalent_to(caf6a)
        assert caf12a.is_canonical_abstract_formula_equivalent_to(caf12a)

        assert not caf1.is_canonical_abstract_formula_equivalent_to(caf2a)
        assert not caf1.is_canonical_abstract_formula_equivalent_to(caf2b)
        assert not caf1.is_canonical_abstract_formula_equivalent_to(caf6a)
        assert not caf1.is_canonical_abstract_formula_equivalent_to(caf12a)

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

    def test_build_formula_from_tree_of_integer_tuple_pairs(self, caf1):
        tree_of_pairs = (0, (),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.CanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((0, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.CanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.CanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (2, (),), (3, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.CanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (0, ((1, ((2, ((3, ((1, (),),),),),),),),),), (4, ((1, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.CanonicalAbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi

    def test_get_sub_tree_by_path(self, caf1, caf2a, caf6a, caf12a, caf_big):
        assert caf1.get_sub_formula_by_path((0,)) == caf1
        assert caf2a.get_sub_formula_by_path((0,)) == caf2a
        assert caf2a.get_sub_formula_by_path((0, 0,)) == caf1

        assert caf_big.get_sub_formula_by_path((0, 3,)) == caf12a
        assert caf_big.get_sub_formula_by_path((0, 3, 2,)) == (0, 1, 2,)
        assert caf_big.get_sub_formula_by_path((0, 3, 2, 4,)) == (0, 1, 2,)
