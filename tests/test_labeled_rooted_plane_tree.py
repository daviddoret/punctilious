import pytest

import punctilious as pu
from conftest import t6_a_aa_ab_ac_ad_ae, t2_a_aa


class TestLabeledRootedPlaneTree:
    def test_construction_success(self):
        phi1 = pu.lrptl.LabeledRootedPlaneTree(t=(((),), (),), s=(1, 2, 3, 4,))
        phi2 = pu.lrptl.LabeledRootedPlaneTree(t=(((),), (),), s=(1, 2, 1, 1,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.lrptl.LabeledRootedPlaneTree(t=(((),), (),), s=(1, 3,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.lrptl.LabeledRootedPlaneTree(t=(((),), (),), s=(1, 2, 1, 3, 1,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.lrptl.LabeledRootedPlaneTree(t=(((),), (),), s=(1, 2, 1, 2, 1, 4, 8, 2))

    def test_is_canonical(self, lrpt1, lrpt3, lrpt4, lrpt6, lrpt7, lrpt8, t1_a, t2_a_aa, t3_a_aa_aaa, t12):
        assert not lrpt1.is_canonical
        assert not lrpt3.is_canonical
        assert not lrpt4.is_canonical
        assert not lrpt6.is_canonical
        assert not lrpt7.is_canonical
        assert lrpt8.is_canonical

        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (0,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (17,))
        assert not phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (0, 0,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (0, 1,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (94, 12,))
        assert not phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (0, 0, 0,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (0, 1, 2,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (9, 5, 104,))
        assert not phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (0, 0, 0,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (0, 1, 2,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (100, 102, 140,))
        assert not phi.is_canonical
        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.lrptl.LabeledRootedPlaneTree(t12, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,))
        assert phi.is_canonical
        phi = pu.lrptl.LabeledRootedPlaneTree(t12, (15, 1, 8, 3, 3, 10, 11, 12, 11, 6, 2, 10,))
        assert not phi.is_canonical

    def test_iterate_immediate_sub_sequences(self, raw_1, raw_2, raw_3, raw_4, raw_5, raw_6, raw_1_1, raw_1_2, lrpt1,
                                             nns0, lrpt3, nns01,
                                             lrpt6,
                                             nns012345,
                                             lrpt7, nns0123456789_10_11):
        l = tuple(t for t in lrpt1.iterate_immediate_sub_sequences())
        assert len(l) == 0
        l = tuple(t for t in lrpt3.iterate_immediate_sub_sequences())
        assert l[0] == raw_1
        l = tuple(t for t in lrpt6.iterate_immediate_sub_sequences())
        assert l[0] == raw_2
        assert l[1] == raw_3
        assert l[2] == raw_4
        assert l[3] == raw_5
        assert l[4] == raw_6
        l = tuple(t for t in lrpt7.iterate_immediate_sub_sequences())
        assert l[0] == raw_2
        assert l[1] == (3, 4,)
        assert l[2] == (5, 6, 7, 8, 9, 10,)
        assert l[3] == (11, 12,)

    def test_iterate_sub_sequences(self, t1_a, t2_a_aa, t3_a_aa_aaa, t7_a_aa_ab_aaa_aaaa_aba_abaa):
        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (1,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 1
        assert l[0] == phi

        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (17,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 1
        assert l[0] == phi

        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (1, 2,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 2
        assert l[0] == phi
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))

        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (4, 3,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 2
        assert l[0] == phi
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (3,))

        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (1, 1, 1,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (1,))
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (1,))

        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (1, 2, 3,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))
        assert l[2] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (3,))

        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 2, 15,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 3
        assert l[0] == phi
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))
        assert l[2] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (15,))

        phi = pu.lrptl.LabeledRootedPlaneTree(t7_a_aa_ab_aaa_aaaa_aba_abaa, (4, 2, 5, 2, 8, 10, 3,))
        l = tuple(t for t in phi.iterate_subtrees())
        assert len(l) == 7
        assert l[0] == phi
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (2, 5, 2,))
        assert l[2] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (5,))
        assert l[3] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))
        assert l[4] == pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (8, 10, 3,))
        assert l[5] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (10,))
        assert l[6] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (3,))

    def test_iterate_immediate_sub_formulas(self, lrpt1, lrpt2, lrpt3, t2_a_aa, lrpt4, lrpt7, lrpt6,
                                            t6_a_aa_ab_ac_ad_ae):
        l = tuple(af for af in lrpt1.iterate_immediate_subtrees())
        assert len(l) == 0
        l = tuple(af for af in lrpt3.iterate_immediate_subtrees())
        assert l[0] == lrpt1
        l = tuple(af for af in lrpt4.iterate_immediate_subtrees())
        assert l[0] == lrpt2
        l = tuple(af for af in lrpt7.iterate_immediate_subtrees())
        assert l[0] == lrpt2
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (3, 4,))
        assert l[2] == pu.lrptl.LabeledRootedPlaneTree(t6_a_aa_ab_ac_ad_ae, (5, 6, 7, 8, 9, 10,))
        assert l[3] == pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (11, 12,))

    def test_iterate_sub_formulas(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, lrpt1, lrpt3, lrpt4, lrpt6, lrpt7):
        l = tuple(t for t in lrpt1.iterate_subtrees())
        assert l[0] == lrpt1
        l = tuple(t for t in lrpt3.iterate_subtrees())
        assert l[0] == lrpt3
        assert l[1] == lrpt1
        l = tuple(t for t in lrpt4.iterate_subtrees())
        assert l[0] == lrpt4
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))
        l = tuple(t for t in lrpt6.iterate_subtrees())
        assert l[0] == lrpt6
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))
        assert l[2] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (3,))
        assert l[3] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (4,))
        assert l[4] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (5,))
        assert l[5] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (6,))
        l = tuple(t for t in lrpt7.iterate_subtrees())
        assert l[0] == lrpt7
        assert l[1] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (2,))
        assert l[2] == pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (3, 4,))
        assert l[3] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (4,))
        assert l[4] == pu.lrptl.LabeledRootedPlaneTree(t6_a_aa_ab_ac_ad_ae, (5, 6, 7, 8, 9, 10,))
        assert l[5] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (6,))
        assert l[6] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (7,))
        assert l[7] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (8,))
        assert l[8] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (9,))
        assert l[9] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (10,))
        assert l[10] == pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (11, 12,))
        assert l[11] == pu.lrptl.LabeledRootedPlaneTree(t1_a, (12,))

    def test_main_sequence_element(self, lrpt1, lrpt3, lrpt4, lrpt6, lrpt7):
        assert lrpt1.main_element == 1
        assert lrpt3.main_element == 1
        assert lrpt4.main_element == 1
        assert lrpt6.main_element == 1
        assert lrpt7.main_element == 1

    def test_tree_size(self, lrpt1, lrpt3, lrpt4, lrpt6, lrpt7):
        assert lrpt1.tree_size == 1
        assert lrpt3.tree_size == 2
        assert lrpt4.tree_size == 2
        assert lrpt6.tree_size == 6
        assert lrpt7.tree_size == 12

    def test_formula_degree(self, lrpt1, lrpt3, lrpt4, lrpt6, lrpt7):
        assert lrpt1.formula_degree == 0
        assert lrpt3.formula_degree == 1
        assert lrpt4.formula_degree == 1
        assert lrpt6.formula_degree == 1
        assert lrpt7.formula_degree == 4

    def test_is_labeled_rooted_plane_tree_equivalent_to(self, lrpt1, lrpt3, lrpt4, lrpt6, lrpt7):
        assert lrpt1.is_labeled_rooted_plane_tree_equivalent_to(lrpt1)
        assert lrpt3.is_labeled_rooted_plane_tree_equivalent_to(lrpt3)
        assert lrpt4.is_labeled_rooted_plane_tree_equivalent_to(lrpt4)
        assert lrpt6.is_labeled_rooted_plane_tree_equivalent_to(lrpt6)
        assert lrpt7.is_labeled_rooted_plane_tree_equivalent_to(lrpt7)

        assert not lrpt1.is_labeled_rooted_plane_tree_equivalent_to(lrpt3)
        assert not lrpt1.is_labeled_rooted_plane_tree_equivalent_to(lrpt4)
        assert not lrpt1.is_labeled_rooted_plane_tree_equivalent_to(lrpt6)
        assert not lrpt1.is_labeled_rooted_plane_tree_equivalent_to(lrpt7)

    def test_extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(self):
        tree_of_pairs = (1, (),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == ((), (1,),)
        tree_of_pairs = (4, ((3, (),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((),), (4, 3,),)
        tree_of_pairs = (4, ((10, (),), (9, (),), (8, (),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((), (), (),), (4, 10, 9, 8,),)
        tree_of_pairs = (4, ((10, (),), (9, ((4, ((3, ((4, ((3, (),),),),),),),),),), (8, ((1, (),),),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert (t, s,) == (((), (((((),),),),), ((),),), (4, 10, 9, 4, 3, 4, 3, 8, 1,),)

    def test_build_formula_from_tree_of_integer_tuple_pairs(self, lrpt1):
        tree_of_pairs = (1, (),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.lrptl.LabeledRootedPlaneTree(t, s)
        psi = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((1, (),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.lrptl.LabeledRootedPlaneTree(t, s)
        psi = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((2, (),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.lrptl.LabeledRootedPlaneTree(t, s)
        psi = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((2, (),), (3, (),), (4, (),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.lrptl.LabeledRootedPlaneTree(t, s)
        psi = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi
        tree_of_pairs = (1, ((2, (),), (1, ((2, ((3, ((4, ((2, (),),),),),),),),),), (5, ((2, (),),),),),)
        t, s = pu.lrptl.extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(tree_of_pairs)
        phi = pu.lrptl.LabeledRootedPlaneTree(t, s)
        psi = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(tree_of_pairs)
        assert phi == psi

    def test_get_sub_formula_by_path(self, lrpt1, lrpt3, lrpt6, lrpt7, lrpt8, t1_a, t6_a_aa_ab_ac_ad_ae, t12):
        assert lrpt1.get_sub_formula_by_path((0,)) == lrpt1
        assert lrpt3.get_sub_formula_by_path((0,)) == lrpt3
        assert lrpt3.get_sub_formula_by_path((0, 0,)) == lrpt1

        assert lrpt8.get_sub_formula_by_path((0, 3,)) == pu.lrptl.LabeledRootedPlaneTree(
            t=t12,
            s=(4, 3, 2, 1, 4, 9, 10, 7, 7, 7, 9, 0))

        assert lrpt8.get_sub_formula_by_path((0, 3, 2,)) == pu.lrptl.LabeledRootedPlaneTree(
            t6_a_aa_ab_ac_ad_ae, (4, 9, 10, 7, 7, 7,)
        )
        assert lrpt8.get_sub_formula_by_path((0, 3, 2, 4,)) == pu.lrptl.LabeledRootedPlaneTree(
            t1_a, (7,))

    def test_represent_as_function(self, t1_a, t2_a_aa, t3_a_aa_aaa, t6_a_aa_ab_ac_ad_ae, t12):
        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (1,))
        assert phi.represent_as_function() == "1"
        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (18,))
        assert phi.represent_as_function() == "18"
        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (1, 1,))
        assert phi.represent_as_function() == "1(1)"
        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (1, 2,))
        assert phi.represent_as_function() == "1(2)"
        phi = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (94, 12,))
        assert phi.represent_as_function() == "94(12)"
        phi = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (1, 1, 1,))
        assert phi.represent_as_function() == "1(1(1))"
        phi = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (1, 2, 3,))
        assert phi.represent_as_function() == "1(2(3))"
        phi = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (9, 5, 104,))
        assert phi.represent_as_function() == "9(5(104))"
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (1, 1, 1,))
        assert phi.represent_as_function() == "1(1, 1)"
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (1, 2, 3,))
        assert phi.represent_as_function() == "1(2, 3)"
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (100, 102, 140,))
        assert phi.represent_as_function() == "100(102, 140)"
        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.lrptl.LabeledRootedPlaneTree(t12, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,))
        assert phi.represent_as_function() == "1(2, 3(4), 5(6, 7, 8, 9, 10), 11(12))"
        phi = pu.lrptl.LabeledRootedPlaneTree(t12, (15, 1, 8, 3, 3, 10, 11, 12, 11, 6, 2, 10,))
        assert phi.represent_as_function() == "15(1, 8(3), 3(10, 11, 12, 11, 6), 2(10))"

    def test_canonical_labeled_rooted_plane_tree(self, t1_a, t2_a_aa, t3_a_aa_aaa, t12):
        t0 = pu.lrptl.LabeledRootedPlaneTree(t1_a, (0,))
        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (1,))
        assert phi.canonical_labeled_rooted_plane_tree == t0
        psi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (17,))
        assert psi.canonical_labeled_rooted_plane_tree == t0

        t00 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (0, 0,))
        phi1 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (1, 1,))
        assert phi1.canonical_labeled_rooted_plane_tree == t00
        psi1 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (13, 13,))
        assert psi1.canonical_labeled_rooted_plane_tree == t00

        t01 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (0, 1,))
        phi2 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (1, 2,))
        assert phi2.canonical_labeled_rooted_plane_tree == t01
        psi2 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (102, 1,))
        assert psi2.canonical_labeled_rooted_plane_tree == t01

        assert phi1.canonical_labeled_rooted_plane_tree != phi2.canonical_labeled_rooted_plane_tree

        t000 = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (0, 0, 0,))
        phi1 = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (1, 1, 1,))
        assert phi1.canonical_labeled_rooted_plane_tree == t000
        psi1 = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (5, 5, 5,))
        assert psi1.canonical_labeled_rooted_plane_tree == t000

        t012 = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (0, 1, 2,))
        phi2 = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (1, 2, 3,))
        assert phi2.canonical_labeled_rooted_plane_tree == t012
        psi2 = pu.lrptl.LabeledRootedPlaneTree(t3_a_aa_aaa, (9, 5, 104,))
        assert psi2.canonical_labeled_rooted_plane_tree == t012

        assert phi1.canonical_labeled_rooted_plane_tree != phi2.canonical_labeled_rooted_plane_tree

        # (t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)
        phi = pu.lrptl.LabeledRootedPlaneTree(t12, (0, 1, 2, 3, 3, 4, 5, 6, 5, 7, 8, 4,))
        assert phi.canonical_labeled_rooted_plane_tree == phi
        psi = pu.lrptl.LabeledRootedPlaneTree(t12, (14, 0, 7, 2, 2, 9, 10, 11, 10, 5, 1, 9,))
        assert psi.canonical_labeled_rooted_plane_tree == phi

    def test_is_subformula_of(self, t1_a, t6_a_aa_ab_ac_ad_ae, lrpt8):
        phi = pu.lrptl.LabeledRootedPlaneTree(t6_a_aa_ab_ac_ad_ae, (4, 9, 10, 7, 7, 7,))
        assert phi.is_sub_formula_of(lrpt8)

        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (12,))
        assert phi.is_sub_formula_of(lrpt8)

        assert not pu.lrptl.LabeledRootedPlaneTree(t6_a_aa_ab_ac_ad_ae,
                                                   (2, 0, 3, 0, 2, 2,)).is_sub_formula_of(lrpt8)

    def test_declare_labeled_rooted_plane_tree_from_immediate_sub_formulas(self, t1_a, t2_a_aa, t3_a_aa_aaa):
        phi1 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (17, 15,))
        phi2 = pu.lrptl.LabeledRootedPlaneTree(t1_a, (31,))
        phi3 = pu.lrptl.LabeledRootedPlaneTree(t2_a_aa, (9, 2,))
        phi4 = pu.lrptl.LabeledRootedPlaneTree.from_immediate_subtrees(n=4, s=(phi1, phi2, phi3,))
        t = pu.rptl.RootedPlaneTree(t2_a_aa, t1_a, t2_a_aa)
        phi5 = pu.lrptl.LabeledRootedPlaneTree(t, (4, 17, 15, 31, 9, 2,))
        assert phi4 == phi5

    def test_canonical_order(self, lrpt1, lrpt2, lrpt3, lrpt4, lrpt5, lrpt6, lrpt7, lrpt8):
        assert lrpt1.is_strictly_less_than(lrpt2)
        assert lrpt3.is_strictly_less_than(lrpt4)
        assert pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 2, 3,)).is_strictly_less_than(
            pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 2, 5,)))

    def test_canonical_order_2(self):
        for i in range(0, 2048):
            phi: pu.lrptl.LabeledRootedPlaneTree
            if i == 0:
                phi = pu.lrptl.RecursiveSequenceOrder.least_element

    def test_is_increasing(self, lrpt1, lrpt2, lrpt3, lrpt4, lrpt5, lrpt6, lrpt7, lrpt8):
        assert lrpt1.is_increasing
        assert lrpt2.is_increasing
        assert lrpt3.is_increasing
        assert lrpt4.is_increasing
        assert lrpt5.is_increasing
        assert lrpt6.is_increasing
        assert not lrpt8.is_increasing
        assert pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 2, 3,)).is_increasing
        assert pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 5, 5,)).is_increasing
        assert not pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 3, 2,)).is_increasing

    def test_is_strictly_increasing(self, lrpt1, lrpt2, lrpt3, lrpt4, lrpt5, lrpt6, lrpt7, lrpt8):
        assert lrpt1.is_strictly_increasing
        assert lrpt2.is_strictly_increasing
        assert lrpt3.is_strictly_increasing
        assert lrpt4.is_strictly_increasing
        assert lrpt5.is_strictly_increasing
        assert lrpt6.is_strictly_increasing
        # assert af_big.is_strictly_increasing
        assert pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 2, 3,)).is_strictly_increasing
        assert not pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 5, 5,)).is_strictly_increasing
        assert not pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (9, 3, 2,)).is_strictly_increasing

    def test_substitute_sub_formulas(self, t1_a, t2_a_aa, t3_a_aa_aaa, t6_a_aa_ab_ac_ad_ae,
                                     t7_a_aa_ab_aaa_aaaa_aba_abaa):
        p = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (17, 38, 59,))
        i = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (25, 11, 42,))
        m: pu.lrptl.LabeledRootedPlaneTree = pu.lrptl.LabeledRootedPlaneTree.abstract_map_from_preimage_and_image(n=51,
                                                                                                                  p=p,
                                                                                                                  i=i)
        phi = pu.lrptl.LabeledRootedPlaneTree(t1_a, (38,))
        psi = phi.substitute_subtrees_with_map(m=m)
        assert psi == pu.lrptl.LabeledRootedPlaneTree(t1_a, (11,))

        p = pu.lrptl.LabeledRootedPlaneTree(t7_a_aa_ab_aaa_aaaa_aba_abaa, (1, 2, 3, 4, 5, 6, 7,))
        i = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (8, 9, 10,))
        m: pu.lrptl.LabeledRootedPlaneTree = pu.lrptl.LabeledRootedPlaneTree.abstract_map_from_preimage_and_image(n=94,
                                                                                                                  p=p,
                                                                                                                  i=i)
        phi = pu.lrptl.LabeledRootedPlaneTree(pu.rptc.t3_a_aa_ab, (5, 6, 7,))
        psi = phi.substitute_subtrees_with_map(m=m)
        assert psi == pu.lrptl.LabeledRootedPlaneTree(t1_a, (10,))

        pass

    def test_least_element(self):
        trivial_formula = pu.lrptl.LRPT(t=pu.rptl.trivial_rooted_plane_tree, s=pu.nn0sl.NaturalNumber0Sequence(0))
        assert pu.lrptl.RecursiveSequenceOrder.least_element == trivial_formula
        assert pu.lrptl.LabeledRootedPlaneTree.least_element == trivial_formula
        assert pu.lrptl.empty_tree == trivial_formula
        assert pu.lrptl.trivial_tree == trivial_formula

    def test_ranking(self):
        t0 = pu.lrptl.LabeledRootedPlaneTree.least_element
        assert t0.rank == 0
        assert pu.lrptl.LabeledRootedPlaneTree.unrank(0) == t0
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_immediate_subtrees(n=0, s=(t0,))
        assert t1.rank == 1
        assert pu.lrptl.LabeledRootedPlaneTree.unrank(1) == t1
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_immediate_subtrees(n=1)
        assert t2.rank == 2
        t2b = pu.lrptl.LabeledRootedPlaneTree.unrank(2)
        assert t2b == t2
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_immediate_subtrees(n=0, s=(t0, t0,))
        assert t3.rank == 3
        assert pu.lrptl.LabeledRootedPlaneTree.unrank(3) == t3
        pass

    def test_successor_unrank_consistency(self):
        for i in range(1024):
            t: pu.lrptl.LabeledRootedPlaneTree
            if i == 0:
                t = pu.lrptl.LabeledRootedPlaneTree.least_element
            else:
                t = t.successor
            t2 = pu.lrptl.LabeledRootedPlaneTree.unrank(i)
            assert t == t2
            r = t.rank
            assert r == i

    def test_super_recursive_order(self):
        # s = (2, 2436, 2322, 4370)
        # s = pu.nn0sl.NaturalNumber0Sequence(*s)
        # n_bad = s.rank()
        # n = pu.nn0sl.RefinedGodelNumberOrder.rank(s)
        # assert n_bad == n
        # s1 = pu.nn0sl.SumFirstLexicographicSecondOrder.unrank(n)
        # s2 = pu.nn0sl.RefinedGodelNumberOrder.unrank(n)

        # l = []
        # for i in range(0, 1024):
        #    l.append(t)
        t0a = pu.lrptl.LabeledRootedPlaneTree.least_element
        t0b = pu.lrptl.LabeledRootedPlaneTree.unrank(0)
        assert t0a == t0b
        r = t0a.rank
        assert t0a.rank == 0
        t1a = t0a.successor
        t1b = pu.lrptl.LabeledRootedPlaneTree.unrank(1)
        assert t1a == t1b
        t2a = t1a.successor
        t2b = pu.lrptl.LabeledRootedPlaneTree.unrank(2)
        assert t2a == t2b
        pass
