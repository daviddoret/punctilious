import pytest

import punctilious as pu
from conftest import t6_a_aa_ab_ac_ad_ae, t2_a_aa


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

    def test_is_canonical(self, af1, af2a, af2b, af6a, af12a, af_big, t1_a, t2_a_aa, t3_a_aa_aaa, t3_a_aa_ab, t12):
        assert af1.is_canonical
        assert af2a.is_canonical
        assert af2b.is_canonical
        assert af6a.is_canonical
        assert af12a.is_canonical
        assert af_big.is_canonical

        phi = pu.afl.AbstractFormula(t1_a, (0,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t1_a, (17,))
        assert not phi.is_canonical
        phi = pu.afl.AbstractFormula(t2_a_aa, (0, 0,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t2_a_aa, (0, 1,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t2_a_aa, (94, 12,))
        assert not phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (0, 0, 0,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (0, 1, 2,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (9, 5, 104,))
        assert not phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (0, 0, 0,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (0, 1, 2,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (100, 102, 140,))
        assert not phi.is_canonical
        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.afl.AbstractFormula(t12, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t12, (14, 0, 7, 2, 2, 9, 10, 11, 10, 5, 1, 9,))
        assert not phi.is_canonical

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

    def test_iterate_sub_sequences(self, t1_a, t2_a_aa, t3_a_aa_aaa, t3_a_aa_ab, t7_a_aa_ab_aaa_aaaa_aba_abaa):
        phi = pu.afl.AbstractFormula(t1_a, (0,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 1
        assert l[0] == phi

        phi = pu.afl.AbstractFormula(t1_a, (17,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 1
        assert l[0] == phi

        phi = pu.afl.AbstractFormula(t2_a_aa, (0, 1,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 2
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))

        phi = pu.afl.AbstractFormula(t2_a_aa, (3, 2,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 2
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))

        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (0, 0, 0,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (0,))
        assert l[1] == pu.afl.AbstractFormula(t1_a, (0,))

        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (0, 1, 2,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (2,))

        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (8, 1, 14,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (14,))

        phi = pu.afl.AbstractFormula(t7_a_aa_ab_aaa_aaaa_aba_abaa, (3, 1, 4, 1, 7, 9, 2,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 7
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t3_a_aa_ab, (1, 4, 1,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (4,))
        assert l[3] == pu.afl.AbstractFormula(t1_a, (1,))
        assert l[4] == pu.afl.AbstractFormula(t3_a_aa_ab, (7, 9, 2,))
        assert l[5] == pu.afl.AbstractFormula(t1_a, (9,))
        assert l[6] == pu.afl.AbstractFormula(t1_a, (2,))

    def test_iterate_immediate_sub_formulas(self, af1, af1b, af2a, t2_a_aa, af2b, af12a, af6a, t6_a_aa_ab_ac_ad_ae):
        l = tuple(af for af in af1.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(af for af in af2a.iterate_immediate_sub_formulas())
        assert l[0] == af1
        l = tuple(af for af in af2b.iterate_immediate_sub_formulas())
        assert l[0] == af1b
        l = tuple(af for af in af12a.iterate_immediate_sub_formulas())
        assert l[0] == af1b
        assert l[1] == pu.afl.AbstractFormula(t2_a_aa, (2, 3,))
        assert l[2] == pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae, (4, 5, 6, 7, 8, 9,))
        assert l[3] == pu.afl.AbstractFormula(t2_a_aa, (10, 11,))

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
        psi = pu.afl.declare_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (2, (),), (3, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (0, ((1, (),), (0, ((1, ((2, ((3, ((1, (),),),),),),),),),), (4, ((1, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.declare_abstract_formula_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi

    def test_get_sub_formula_by_path(self, af1, af2a, af6a, af12a, af_big, t1_a, t6_a_aa_ab_ac_ad_ae, t12):
        assert af1.get_sub_formula_by_path((0,)) == af1
        assert af2a.get_sub_formula_by_path((0,)) == af2a
        assert af2a.get_sub_formula_by_path((0, 0,)) == af1

        assert af_big.get_sub_formula_by_path((0, 3,)) == pu.afl.AbstractFormula(
            t=t12,
            s=(4, 3, 2, 1, 4, 9, 10, 7, 7, 7, 9, 0))

        assert af_big.get_sub_formula_by_path((0, 3, 2,)) == pu.afl.AbstractFormula(
            t6_a_aa_ab_ac_ad_ae, (4, 9, 10, 7, 7, 7,)
        )
        assert af_big.get_sub_formula_by_path((0, 3, 2, 4,)) == pu.afl.AbstractFormula(
            t1_a, (7,))

    def test_represent_as_function(self, t1_a, t2_a_aa, t3_a_aa_aaa, t3_a_aa_ab, t6_a_aa_ab_ac_ad_ae, t12):
        phi = pu.afl.AbstractFormula(t1_a, (0,))
        assert phi.represent_as_function() == "0"
        phi = pu.afl.AbstractFormula(t1_a, (17,))
        assert phi.represent_as_function() == "17"
        phi = pu.afl.AbstractFormula(t2_a_aa, (0, 0,))
        assert phi.represent_as_function() == "0(0)"
        phi = pu.afl.AbstractFormula(t2_a_aa, (0, 1,))
        assert phi.represent_as_function() == "0(1)"
        phi = pu.afl.AbstractFormula(t2_a_aa, (94, 12,))
        assert phi.represent_as_function() == "94(12)"
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (0, 0, 0,))
        assert phi.represent_as_function() == "0(0(0))"
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (0, 1, 2,))
        assert phi.represent_as_function() == "0(1(2))"
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (9, 5, 104,))
        assert phi.represent_as_function() == "9(5(104))"
        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (0, 0, 0,))
        assert phi.represent_as_function() == "0(0, 0)"
        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (0, 1, 2,))
        assert phi.represent_as_function() == "0(1, 2)"
        phi = pu.afl.AbstractFormula(t3_a_aa_ab, (100, 102, 140,))
        assert phi.represent_as_function() == "100(102, 140)"
        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.afl.AbstractFormula(t12, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,))
        assert phi.represent_as_function() == "0(1, 2(3), 4(5, 6, 7, 8, 9), 10(11))"
        phi = pu.afl.AbstractFormula(t12, (14, 0, 7, 2, 2, 9, 10, 11, 10, 5, 1, 9,))
        assert phi.represent_as_function() == "14(0, 7(2), 2(9, 10, 11, 10, 5), 1(9))"

    def test_canonical_abstract_formula(self, t1_a, t2_a_aa, t3_a_aa_aaa, t3_a_aa_ab, t12):
        phi = pu.afl.AbstractFormula(t1_a, (0,))
        assert phi.canonical_abstract_formula == phi
        psi = pu.afl.AbstractFormula(t1_a, (17,))
        assert psi.canonical_abstract_formula == phi

        phi1 = pu.afl.AbstractFormula(t2_a_aa, (0, 0,))
        assert phi1.canonical_abstract_formula == phi1
        psi1 = pu.afl.AbstractFormula(t2_a_aa, (13, 13,))
        assert psi1.canonical_abstract_formula == phi1

        phi2 = pu.afl.AbstractFormula(t2_a_aa, (0, 1,))
        assert phi2.canonical_abstract_formula == phi2
        psi2 = pu.afl.AbstractFormula(t2_a_aa, (102, 1,))
        assert psi2.canonical_abstract_formula == phi2

        assert phi1.canonical_abstract_formula != phi2.canonical_abstract_formula

        phi1 = pu.afl.AbstractFormula(t3_a_aa_aaa, (0, 0, 0,))
        assert phi1.canonical_abstract_formula == phi1
        psi1 = pu.afl.AbstractFormula(t3_a_aa_aaa, (5, 5, 5,))
        assert psi1.canonical_abstract_formula == phi1

        phi2 = pu.afl.AbstractFormula(t3_a_aa_aaa, (0, 1, 2,))
        assert phi2.canonical_abstract_formula == phi2
        psi2 = pu.afl.AbstractFormula(t3_a_aa_aaa, (9, 5, 104,))
        assert psi2.canonical_abstract_formula == phi2

        assert phi1.canonical_abstract_formula != phi2.canonical_abstract_formula

        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.afl.AbstractFormula(t12, (0, 1, 2, 3, 3, 4, 5, 6, 5, 7, 8, 4,))
        assert phi.canonical_abstract_formula == phi
        psi = pu.afl.AbstractFormula(t12, (14, 0, 7, 2, 2, 9, 10, 11, 10, 5, 1, 9,))
        assert psi.canonical_abstract_formula == phi

    def test_is_subformula_of(self, t1_a, t6_a_aa_ab_ac_ad_ae, af_big):
        phi = pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae, (4, 9, 10, 7, 7, 7,))
        assert phi.is_sub_formula_of(af_big)

        phi = pu.afl.AbstractFormula(t1_a, (12,))
        assert phi.is_sub_formula_of(af_big)

        assert not pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae,
                                          (2, 0, 3, 0, 2, 2,)).is_sub_formula_of(af_big)
