import pytest

import punctilious as pu


class TestAbstractFormula:
    def test_construction_success(self):
        phi1 = pu.afl.AbstractFormula(t=(((),), (),), s=(0, 1, 2, 3,))
        phi2 = pu.afl.AbstractFormula(t=(((),), (),), s=(0, 1, 0, 0,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.AbstractFormula(t=(((),), (),), s=(0, 2,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.AbstractFormula(t=(((),), (),), s=(0, 1, 0, 2, 0,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.AbstractFormula(t=(((),), (),), s=(0, 1, 0, 1, 0, 3, 7, 1))

    def test_iterate_immediate_sub_sequences(self, s0, s1, s2, s3, s4, s5, s00, s01, af1, nns0, af2a, nns01,
                                             af6a,
                                             nns012345,
                                             af12a, nns0123456789_10_11):
        l = tuple(t for t in af1.iterate_immediate_sub_sequences())
        assert len(l) == 0
        l = tuple(t for t in af2a.iterate_immediate_sub_sequences())
        assert l[0] == s0
        l = tuple(t for t in af6a.iterate_immediate_sub_sequences())
        assert l[0] == s1
        assert l[1] == s2
        assert l[2] == s3
        assert l[3] == s4
        assert l[4] == s5
        l = tuple(t for t in af12a.iterate_immediate_sub_sequences())
        assert l[0] == s1
        assert l[1] == (2, 3,)
        assert l[2] == (4, 5, 6, 7, 8, 9,)
        assert l[3] == (10, 11,)

    def test_iterate_immediate_sub_natural_numbers_sequences(self, af1, nns0, af2a, nns01, af6a,
                                                             nns012345,
                                                             af12a, nns0123456789_10_11):
        l = tuple(t for t in af1.iterate_immediate_sub_restricted_growth_function_sequences())
        assert len(l) == 0
        l = tuple(t for t in af2a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == nns0
        l = tuple(t for t in af6a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == nns0
        assert l[1] == nns0
        assert l[2] == nns0
        assert l[3] == nns0
        assert l[4] == nns0
        l = tuple(t for t in af12a.iterate_immediate_sub_restricted_growth_function_sequences())
        assert l[0] == nns0
        assert l[1] == nns01
        assert l[2] == nns012345
        assert l[3] == nns01

    def test_iterate_sub_sequences(self, af1, nns0, af2a, nns01, af6a, af12a,
                                   nns012345):
        l = tuple(t for t in af1.iterate_sub_sequences())
        assert l[0] == af1.natural_numbers_sequence
        l = tuple(t for t in af2a.iterate_sub_sequences())
        assert l[0] == af2a.natural_numbers_sequence
        assert l[1] == nns0
        l = tuple(t for t in af6a.iterate_sub_sequences())
        assert l[0] == af6a.natural_numbers_sequence
        assert l[1] == pu.sl.NaturalNumberSequence(1, )
        assert l[2] == pu.sl.NaturalNumberSequence(2, )
        assert l[3] == pu.sl.NaturalNumberSequence(3, )
        assert l[4] == pu.sl.NaturalNumberSequence(4, )
        assert l[5] == pu.sl.NaturalNumberSequence(5, )
        l = tuple(t for t in af12a.iterate_sub_sequences())
        assert l[0] == af12a.natural_numbers_sequence
        assert l[1] == pu.sl.NaturalNumberSequence(1, )
        assert l[2] == pu.sl.NaturalNumberSequence(2, 3, )
        assert l[3] == pu.sl.NaturalNumberSequence(3, )
        assert l[4] == pu.sl.NaturalNumberSequence(4, 5, 6, 7, 8, 9, )
        assert l[5] == pu.sl.NaturalNumberSequence(5, )
        assert l[6] == pu.sl.NaturalNumberSequence(6, )
        assert l[7] == pu.sl.NaturalNumberSequence(7, )
        assert l[8] == pu.sl.NaturalNumberSequence(8, )
        assert l[9] == pu.sl.NaturalNumberSequence(9, )
        assert l[10] == pu.sl.NaturalNumberSequence(10, 11, )
        assert l[11] == pu.sl.NaturalNumberSequence(11, )

    def test_iterate_immediate_sub_formulas(self, af1, af2a, af2b, af12a, af6a):
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

    def test_iterate_sub_formulas(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, af1, af2a, af2b, af6a, af12a):
        l = tuple(t for t in af1.iterate_sub_formulas())
        assert l[0] == af1
        l = tuple(t for t in af2a.iterate_sub_formulas())
        assert l[0] == af2a
        assert l[1] == af1
        l = tuple(t for t in af2b.iterate_sub_formulas())
        assert l[0] == af2b
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))
        l = tuple(t for t in af6a.iterate_sub_formulas())
        assert l[0] == af6a
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (2,))
        assert l[3] == pu.afl.AbstractFormula(t1_a, (3,))
        assert l[4] == pu.afl.AbstractFormula(t1_a, (4,))
        assert l[5] == pu.afl.AbstractFormula(t1_a, (5,))
        l = tuple(t for t in af12a.iterate_sub_formulas())
        assert l[0] == af12a
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))
        assert l[2] == pu.afl.AbstractFormula(t2_a_aa, (2, 3,))
        assert l[3] == pu.afl.AbstractFormula(t1_a, (3,))
        assert l[4] == pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae, (4, 5, 6, 7, 8, 9,))
        assert l[5] == pu.afl.AbstractFormula(t1_a, (5,))
        assert l[6] == pu.afl.AbstractFormula(t1_a, (6,))
        assert l[7] == pu.afl.AbstractFormula(t1_a, (7,))
        assert l[8] == pu.afl.AbstractFormula(t1_a, (8,))
        assert l[9] == pu.afl.AbstractFormula(t1_a, (9,))
        assert l[10] == pu.afl.AbstractFormula(t2_a_aa, (10, 11,))
        assert l[11] == pu.afl.AbstractFormula(t1_a, (11,))

    def test_main_sequence_element(self, af1, af2a, af2b, af6a, af12a):
        assert af1.main_element == 0
        assert af2a.main_element == 0
        assert af2b.main_element == 0
        assert af6a.main_element == 0
        assert af12a.main_element == 0

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

    def test_build_formula_from_tree_of_integer_tuple_pairs(self, af1):
        tree_of_pairs = (0, (),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((0, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (2, (),), (3, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (0, ((1, ((2, ((3, ((1, (),),),),),),),),),), (4, ((1, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi

    def test_get_sub_formula_by_path(self, af1, af2a, af6a, af12a, af_big):
        assert af1.get_sub_formula_by_path((0,)) == af1
        assert af2a.get_sub_formula_by_path((0,)) == af2a
        assert af2a.get_sub_formula_by_path((0, 0,)) == af1

        assert af_big.get_sub_formula_by_path((0, 3,)) == af12a
        assert af_big.get_sub_formula_by_path((0, 3, 2,)) == (0, 1, 2,)
        assert af_big.get_sub_formula_by_path((0, 3, 2, 4,)) == (0, 1, 2,)
