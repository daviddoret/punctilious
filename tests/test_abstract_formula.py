import pytest

import punctilious as pu
from conftest import t6_a_aa_ab_ac_ad_ae, t2_a_aa


class TestAbstractFormula:
    def test_construction_success(self):
        phi1 = pu.afl.AbstractFormula(t=(((),), (),), s=(1, 2, 3, 4,))
        phi2 = pu.afl.AbstractFormula(t=(((),), (),), s=(1, 2, 1, 1,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.AbstractFormula(t=(((),), (),), s=(1, 3,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.AbstractFormula(t=(((),), (),), s=(1, 2, 1, 3, 1,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.afl.AbstractFormula(t=(((),), (),), s=(1, 2, 1, 2, 1, 4, 8, 2))

    def test_is_canonical(self, af1, af2a, af2b, af6a, af12a, af_big, t1_a, t2_a_aa, t3_a_aa_aaa, t12):
        assert af1.is_canonical
        assert af2a.is_canonical
        assert af2b.is_canonical
        assert af6a.is_canonical
        assert af12a.is_canonical
        assert af_big.is_canonical

        phi = pu.afl.AbstractFormula(t1_a, (1,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t1_a, (17,))
        assert not phi.is_canonical
        phi = pu.afl.AbstractFormula(t2_a_aa, (1, 1,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t2_a_aa, (1, 2,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t2_a_aa, (94, 12,))
        assert not phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (1, 1, 1,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (1, 2, 3,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (9, 5, 104,))
        assert not phi.is_canonical
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (1, 1, 1,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (1, 2, 3,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (100, 102, 140,))
        assert not phi.is_canonical
        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.afl.AbstractFormula(t12, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,))
        assert phi.is_canonical
        phi = pu.afl.AbstractFormula(t12, (15, 1, 8, 3, 3, 10, 11, 12, 11, 6, 2, 10,))
        assert not phi.is_canonical

    def test_iterate_immediate_sub_sequences(self, raw_1, raw_2, raw_3, raw_4, raw_5, raw_6, raw_1_1, raw_1_2, af1,
                                             nns0, af2a, nns01,
                                             af6a,
                                             nns012345,
                                             af12a, nns0123456789_10_11):
        l = tuple(t for t in af1.iterate_immediate_sub_sequences())
        assert len(l) == 0
        l = tuple(t for t in af2a.iterate_immediate_sub_sequences())
        assert l[0] == raw_1
        l = tuple(t for t in af6a.iterate_immediate_sub_sequences())
        assert l[0] == raw_2
        assert l[1] == raw_3
        assert l[2] == raw_4
        assert l[3] == raw_5
        assert l[4] == raw_6
        l = tuple(t for t in af12a.iterate_immediate_sub_sequences())
        assert l[0] == raw_2
        assert l[1] == (3, 4,)
        assert l[2] == (5, 6, 7, 8, 9, 10,)
        assert l[3] == (11, 12,)

    def test_iterate_sub_sequences(self, t1_a, t2_a_aa, t3_a_aa_aaa, t7_a_aa_ab_aaa_aaaa_aba_abaa):
        phi = pu.afl.AbstractFormula(t1_a, (1,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 1
        assert l[0] == phi

        phi = pu.afl.AbstractFormula(t1_a, (17,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 1
        assert l[0] == phi

        phi = pu.afl.AbstractFormula(t2_a_aa, (1, 2,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 2
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))

        phi = pu.afl.AbstractFormula(t2_a_aa, (4, 3,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 2
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (3,))

        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (1, 1, 1,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))
        assert l[1] == pu.afl.AbstractFormula(t1_a, (1,))

        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (1, 2, 3,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (3,))

        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 2, 15,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (15,))

        phi = pu.afl.AbstractFormula(t7_a_aa_ab_aaa_aaaa_aba_abaa, (4, 2, 5, 2, 8, 10, 3,))
        l = tuple(t for t in phi.iterate_sub_formulas())
        assert len(l) == 7
        assert l[0] == phi
        assert l[1] == pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (2, 5, 2,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (5,))
        assert l[3] == pu.afl.AbstractFormula(t1_a, (2,))
        assert l[4] == pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (8, 10, 3,))
        assert l[5] == pu.afl.AbstractFormula(t1_a, (10,))
        assert l[6] == pu.afl.AbstractFormula(t1_a, (3,))

    def test_iterate_immediate_sub_formulas(self, af1, af1b, af2a, t2_a_aa, af2b, af12a, af6a, t6_a_aa_ab_ac_ad_ae):
        l = tuple(af for af in af1.iterate_immediate_sub_formulas())
        assert len(l) == 0
        l = tuple(af for af in af2a.iterate_immediate_sub_formulas())
        assert l[0] == af1
        l = tuple(af for af in af2b.iterate_immediate_sub_formulas())
        assert l[0] == af1b
        l = tuple(af for af in af12a.iterate_immediate_sub_formulas())
        assert l[0] == af1b
        assert l[1] == pu.afl.AbstractFormula(t2_a_aa, (3, 4,))
        assert l[2] == pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae, (5, 6, 7, 8, 9, 10,))
        assert l[3] == pu.afl.AbstractFormula(t2_a_aa, (11, 12,))

    def test_iterate_sub_formulas(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, af1, af2a, af2b, af6a, af12a):
        l = tuple(t for t in af1.iterate_sub_formulas())
        assert l[0] == af1
        l = tuple(t for t in af2a.iterate_sub_formulas())
        assert l[0] == af2a
        assert l[1] == af1
        l = tuple(t for t in af2b.iterate_sub_formulas())
        assert l[0] == af2b
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))
        l = tuple(t for t in af6a.iterate_sub_formulas())
        assert l[0] == af6a
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))
        assert l[2] == pu.afl.AbstractFormula(t1_a, (3,))
        assert l[3] == pu.afl.AbstractFormula(t1_a, (4,))
        assert l[4] == pu.afl.AbstractFormula(t1_a, (5,))
        assert l[5] == pu.afl.AbstractFormula(t1_a, (6,))
        l = tuple(t for t in af12a.iterate_sub_formulas())
        assert l[0] == af12a
        assert l[1] == pu.afl.AbstractFormula(t1_a, (2,))
        assert l[2] == pu.afl.AbstractFormula(t2_a_aa, (3, 4,))
        assert l[3] == pu.afl.AbstractFormula(t1_a, (4,))
        assert l[4] == pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae, (5, 6, 7, 8, 9, 10,))
        assert l[5] == pu.afl.AbstractFormula(t1_a, (6,))
        assert l[6] == pu.afl.AbstractFormula(t1_a, (7,))
        assert l[7] == pu.afl.AbstractFormula(t1_a, (8,))
        assert l[8] == pu.afl.AbstractFormula(t1_a, (9,))
        assert l[9] == pu.afl.AbstractFormula(t1_a, (10,))
        assert l[10] == pu.afl.AbstractFormula(t2_a_aa, (11, 12,))
        assert l[11] == pu.afl.AbstractFormula(t1_a, (12,))

    def test_main_sequence_element(self, af1, af2a, af2b, af6a, af12a):
        assert af1.main_element == 1
        assert af2a.main_element == 1
        assert af2b.main_element == 1
        assert af6a.main_element == 1
        assert af12a.main_element == 1

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
        tree_of_pairs = (1, (),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == ((), (1,),)
        tree_of_pairs = (4, ((3, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((),), (4, 3,),)
        tree_of_pairs = (4, ((10, (),), (9, (),), (8, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((), (), (),), (4, 10, 9, 8,),)
        tree_of_pairs = (4, ((10, (),), (9, ((4, ((3, ((4, ((3, (),),),),),),),),),), (8, ((1, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((), (((((),),),),), ((),),), (4, 10, 9, 4, 3, 4, 3, 8, 1,),)

    def test_build_formula_from_tree_of_integer_tuple_pairs(self, af1):
        tree_of_pairs = (1, (),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.AbstractFormula.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((1, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.AbstractFormula.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((2, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.AbstractFormula.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((2, (),), (3, (),), (4, (),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.AbstractFormula.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((2, (),), (1, ((2, ((3, ((4, ((2, (),),),),),),),),),), (5, ((2, (),),),),),)
        t, s = pu.afl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.afl.AbstractFormula(t, s)
        psi = pu.afl.AbstractFormula.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi

    def test_get_sub_formula_by_path(self, af1, af2a, af6a, af12a, af_big, t1_a, t6_a_aa_ab_ac_ad_ae, t12):
        assert af1.get_sub_formula_by_path((1,)) == af1
        assert af2a.get_sub_formula_by_path((1,)) == af2a
        assert af2a.get_sub_formula_by_path((1, 1,)) == af1

        assert af_big.get_sub_formula_by_path((1, 4,)) == pu.afl.AbstractFormula(
            t=t12,
            s=(5, 4, 3, 2, 5, 10, 11, 8, 8, 8, 10, 1))

        assert af_big.get_sub_formula_by_path((1, 4, 3,)) == pu.afl.AbstractFormula(
            t6_a_aa_ab_ac_ad_ae, (5, 10, 11, 8, 8, 8,)
        )
        assert af_big.get_sub_formula_by_path((1, 4, 3, 5,)) == pu.afl.AbstractFormula(
            t1_a, (8,))

    def test_represent_as_function(self, t1_a, t2_a_aa, t3_a_aa_aaa, t6_a_aa_ab_ac_ad_ae, t12):
        phi = pu.afl.AbstractFormula(t1_a, (1,))
        assert phi.represent_as_function() == "1"
        phi = pu.afl.AbstractFormula(t1_a, (18,))
        assert phi.represent_as_function() == "18"
        phi = pu.afl.AbstractFormula(t2_a_aa, (1, 1,))
        assert phi.represent_as_function() == "1(1)"
        phi = pu.afl.AbstractFormula(t2_a_aa, (1, 2,))
        assert phi.represent_as_function() == "1(2)"
        phi = pu.afl.AbstractFormula(t2_a_aa, (94, 12,))
        assert phi.represent_as_function() == "94(12)"
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (1, 1, 1,))
        assert phi.represent_as_function() == "1(1(1))"
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (1, 2, 3,))
        assert phi.represent_as_function() == "1(2(3))"
        phi = pu.afl.AbstractFormula(t3_a_aa_aaa, (9, 5, 104,))
        assert phi.represent_as_function() == "9(5(104))"
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (1, 1, 1,))
        assert phi.represent_as_function() == "1(1, 1)"
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (1, 2, 3,))
        assert phi.represent_as_function() == "1(2, 3)"
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (100, 102, 140,))
        assert phi.represent_as_function() == "100(102, 140)"
        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.afl.AbstractFormula(t12, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,))
        assert phi.represent_as_function() == "1(2, 3(4), 5(6, 7, 8, 9,10), 11(12))"
        phi = pu.afl.AbstractFormula(t12, (15, 1, 8, 3, 3, 10, 11, 12, 11, 6, 2, 10,))
        assert phi.represent_as_function() == "15(1, 8(3), 3(10, 11, 12, 11, 6), 2(10))"

    def test_canonical_abstract_formula(self, t1_a, t2_a_aa, t3_a_aa_aaa, t12):
        phi = pu.afl.AbstractFormula(t1_a, (1,))
        assert phi.canonical_abstract_formula == phi
        psi = pu.afl.AbstractFormula(t1_a, (17,))
        assert psi.canonical_abstract_formula == phi

        phi1 = pu.afl.AbstractFormula(t2_a_aa, (1, 1,))
        assert phi1.canonical_abstract_formula == phi1
        psi1 = pu.afl.AbstractFormula(t2_a_aa, (13, 13,))
        assert psi1.canonical_abstract_formula == phi1

        phi2 = pu.afl.AbstractFormula(t2_a_aa, (1, 2,))
        assert phi2.canonical_abstract_formula == phi2
        psi2 = pu.afl.AbstractFormula(t2_a_aa, (102, 1,))
        assert psi2.canonical_abstract_formula == phi2

        assert phi1.canonical_abstract_formula != phi2.canonical_abstract_formula

        phi1 = pu.afl.AbstractFormula(t3_a_aa_aaa, (1, 1, 1,))
        assert phi1.canonical_abstract_formula == phi1
        psi1 = pu.afl.AbstractFormula(t3_a_aa_aaa, (5, 5, 5,))
        assert psi1.canonical_abstract_formula == phi1

        phi2 = pu.afl.AbstractFormula(t3_a_aa_aaa, (1, 2, 3,))
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

    def test_declare_abstract_formula_from_immediate_sub_formulas(self, t1_a, t2_a_aa, t3_a_aa_aaa):
        phi1 = pu.afl.AbstractFormula(t2_a_aa, (17, 15,))
        phi2 = pu.afl.AbstractFormula(t1_a, (31,))
        phi3 = pu.afl.AbstractFormula(t2_a_aa, (9, 2,))
        phi4 = pu.afl.AbstractFormula.from_immediate_sub_formulas(n=4, s=(phi1, phi2, phi3,))
        t = pu.rptl.RootedPlaneTree(t2_a_aa, t1_a, t2_a_aa)
        phi5 = pu.afl.AbstractFormula(t, (4, 17, 15, 31, 9, 2,))
        assert phi4 == phi5

    def test_canonical_order(self, af1, af1b, af2a, af2b, af3a, af6a, af12a, af_big):
        assert not af1.is_strictly_less_than(af1b)
        assert not af2a.is_strictly_less_than(af2b)
        assert pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 2, 3,)).is_strictly_less_than(
            pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 2, 5,)))

    def test_canonical_order_2(self):
        for i in range(0, 2048):
            phi: pu.afl.AbstractFormula
            if i == 0:
                phi = pu.afl.RecursiveSequenceOrder.least_element

    def test_is_increasing(self, af1, af1b, af2a, af2b, af3a, af6a, af12a, af_big):
        assert af1.is_increasing
        assert af1b.is_increasing
        assert af2a.is_increasing
        assert af2b.is_increasing
        assert af3a.is_increasing
        assert af6a.is_increasing
        assert not af_big.is_increasing
        assert pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 2, 3,)).is_increasing
        assert pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 5, 5,)).is_increasing
        assert not pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 3, 2,)).is_increasing

    def test_is_strictly_increasing(self, af1, af1b, af2a, af2b, af3a, af6a, af12a, af_big):
        assert af1.is_strictly_increasing
        assert af1b.is_strictly_increasing
        assert af2a.is_strictly_increasing
        assert af2b.is_strictly_increasing
        assert af3a.is_strictly_increasing
        assert af6a.is_strictly_increasing
        assert af_big.is_strictly_increasing
        assert pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 2, 3,)).is_strictly_increasing
        assert not pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 5, 5,)).is_strictly_increasing
        assert pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (9, 3, 2,)).is_strictly_increasing

    def test_substitute_sub_formulas(self, t1_a, t2_a_aa, t3_a_aa_aaa, t6_a_aa_ab_ac_ad_ae,
                                     t7_a_aa_ab_aaa_aaaa_aba_abaa):
        p = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (17, 38, 59,))
        i = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (25, 11, 42,))
        m: pu.afl.AbstractFormula = pu.afl.AbstractFormula.abstract_map_from_preimage_and_image(n=51, p=p, i=i)
        phi = pu.afl.AbstractFormula(t1_a, (38,))
        psi = phi.substitute_sub_formulas_with_map(m=m)
        assert psi == pu.afl.AbstractFormula(t1_a, (11,))

        p = pu.afl.AbstractFormula(t7_a_aa_ab_aaa_aaaa_aba_abaa, (1, 2, 3, 4, 5, 6, 7,))
        i = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (8, 9, 10,))
        m: pu.afl.AbstractFormula = pu.afl.AbstractFormula.abstract_map_from_preimage_and_image(n=94, p=p, i=i)
        phi = pu.afl.AbstractFormula(pu.rptc.t3_a_aa_ab, (5, 6, 7,))
        psi = phi.substitute_sub_formulas_with_map(m=m)
        assert psi == pu.afl.AbstractFormula(t1_a, (10,))

        pass

    def test_least_element(self):
        trivial_formula = pu.afl.AF(t=pu.rptl.trivial_rooted_plane_tree, s=pu.nn0sl.NaturalNumber0Sequence(0))
        assert pu.afl.RecursiveSequenceOrder.least_element == trivial_formula
        assert pu.afl.AbstractFormula.least_element == trivial_formula
        assert pu.afl.empty_formula == trivial_formula
        assert pu.afl.trivial_formula == trivial_formula

    def test_ranking(self):
        t0 = pu.afl.AbstractFormula.least_element
        assert t0.rank() == 0
        t1 = pu.afl.AbstractFormula.from_immediate_sub_formulas(n=0, s=(t0,))
        assert t1.rank() == 1

    def test_successor_unrank_consistency(self):
        for i in range(1024):
            t: pu.afl.AbstractFormula
            if i == 0:
                t = pu.afl.AbstractFormula.least_element
            else:
                t = t.successor()
            t2 = pu.afl.AbstractFormula.unrank(i)
            assert t == t2
            r = t.rank()
            assert r == i

    def test_super_recursive_order(self):
        # s = (2, 2436, 2322, 4370)
        # s = pu.nn0sl.NaturalNumber0Sequence(*s)
        # n_bad = s.rank()
        # n = pu.nn0sl.RefinedGodelNumberOrder.rank(s)
        # assert n_bad == n
        # s1 = pu.nn0sl.SumFirstLexicographicSecondOrder.unrank(n)
        # s2 = pu.nn0sl.RefinedGodelNumberOrder.unrank(n)
        # t = pu.afl.AbstractFormula.unrank(n)
        # pass

        # l = []
        # for i in range(0, 1024):
        #    t = pu.afl.AbstractFormula.unrank(i)
        #    l.append(t)
        t0a = pu.afl.AbstractFormula.least_element
        t0b = pu.afl.AbstractFormula.unrank(0)
        assert t0a == t0b
        r = t0a.rank()
        assert t0a.rank() == 0
        t1a = t0a.successor()
        t1b = pu.afl.AbstractFormula.unrank(1)
        assert t1a == t1b
        t2a = t1a.successor()
        t2b = pu.afl.AbstractFormula.unrank(2)
        assert t2a == t2b
        pass
