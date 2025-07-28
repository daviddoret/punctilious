import punctilious as pu


class TestRootedPlaneTree:

    def test_is_rooted_plane_tree_equivalent(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        assert t1_a.is_rooted_plane_tree_equivalent_to(t1_a)
        assert t2_a_aa.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)
        assert t12.is_rooted_plane_tree_equivalent_to(t12)

        assert not t1_a.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert not t1_a.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)
        assert not t1_a.is_rooted_plane_tree_equivalent_to(t12)

        assert not t2_a_aa.is_rooted_plane_tree_equivalent_to(t1_a)
        assert not t2_a_aa.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)
        assert not t2_a_aa.is_rooted_plane_tree_equivalent_to(t12)

        assert not t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t1_a)
        assert not t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert not t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t12)

        assert not t12.is_rooted_plane_tree_equivalent_to(t1_a)
        assert not t12.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert not t12.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)

    def test_is_leaf(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        assert t1_a.is_leaf
        assert not t2_a_aa.is_leaf
        assert not t6_a_aa_ab_ac_ad_ae.is_leaf
        assert not t12.is_leaf

    def test_degree(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        assert t1_a.degree == 0
        assert t2_a_aa.degree == 1
        assert t6_a_aa_ab_ac_ad_ae.degree == 5
        assert t12.degree == 4

    def test_size(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        assert t1_a.size == 1
        assert t2_a_aa.size == 2
        assert t6_a_aa_ab_ac_ad_ae.size == 6
        assert t12.size == 12

    def test_dyck_word(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        assert t1_a.dyck_word == "()"
        assert t2_a_aa.dyck_word == "(())"
        assert t6_a_aa_ab_ac_ad_ae.dyck_word == "(()()()()())"
        assert t12.dyck_word == "(()(())(()()()()())(()))"

    def test_is_rooted_plane_tree_equivalent_to(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        # equivalence with self
        assert t1_a.is_rooted_plane_tree_equivalent_to(t1_a)
        assert t2_a_aa.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)
        assert t12.is_rooted_plane_tree_equivalent_to(t12)
        # non-equivalences
        assert not t1_a.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert not t1_a.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)
        assert not t1_a.is_rooted_plane_tree_equivalent_to(t12)
        assert not t2_a_aa.is_rooted_plane_tree_equivalent_to(t1_a)
        assert not t2_a_aa.is_rooted_plane_tree_equivalent_to(t6_a_aa_ab_ac_ad_ae)
        assert not t2_a_aa.is_rooted_plane_tree_equivalent_to(t12)
        assert not t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t1_a)
        assert not t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert not t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(t12)
        assert not t12.is_rooted_plane_tree_equivalent_to(t1_a)
        assert not t12.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        assert not t12.is_rooted_plane_tree_equivalent_to(t2_a_aa)
        # equivalence with distinct instances
        assert t1_a.is_rooted_plane_tree_equivalent_to(pu.rptl.RootedPlaneTree())
        assert t2_a_aa.is_rooted_plane_tree_equivalent_to(pu.rptl.RootedPlaneTree(t1_a))
        assert t6_a_aa_ab_ac_ad_ae.is_rooted_plane_tree_equivalent_to(
            pu.rptl.RootedPlaneTree(t1_a, t1_a, t1_a, t1_a, t1_a))
        assert t12.is_rooted_plane_tree_equivalent_to(
            pu.rptl.RootedPlaneTree(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa))

    def test_cache(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        t1_clone = pu.rptl.RootedPlaneTree()
        assert t1_a == t1_clone
        assert t1_a is t1_clone
        t2_clone = pu.rptl.RootedPlaneTree(t1_clone)
        assert t2_a_aa == t2_clone
        assert t2_a_aa is t2_clone
        t3_clone = pu.rptl.RootedPlaneTree(t1_clone, t1_clone, t1_clone, t1_clone, t1_clone)
        assert t6_a_aa_ab_ac_ad_ae == t3_clone
        assert t6_a_aa_ab_ac_ad_ae is t3_clone
        t4_clone = pu.rptl.RootedPlaneTree(t1_clone, t2_clone, t3_clone, t2_clone)
        assert t12 == t4_clone
        assert t12 is t4_clone
        pass

    def test_select_sub_rooted_plane_tree_from_path_sequence(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        assert t1_a.select_sub_tree_from_path_sequence((1,)) == t1_a
        assert t2_a_aa.select_sub_tree_from_path_sequence((1,)) == t2_a_aa
        assert t2_a_aa.select_sub_tree_from_path_sequence((1, 1,)) == t1_a
        assert t6_a_aa_ab_ac_ad_ae.select_sub_tree_from_path_sequence((1,)) == t6_a_aa_ab_ac_ad_ae
        assert t6_a_aa_ab_ac_ad_ae.select_sub_tree_from_path_sequence((1, 1,)) == t1_a
        assert t6_a_aa_ab_ac_ad_ae.select_sub_tree_from_path_sequence((1, 2,)) == t1_a
        assert t6_a_aa_ab_ac_ad_ae.select_sub_tree_from_path_sequence((1, 3,)) == t1_a
        assert t6_a_aa_ab_ac_ad_ae.select_sub_tree_from_path_sequence((1, 4,)) == t1_a
        assert t6_a_aa_ab_ac_ad_ae.select_sub_tree_from_path_sequence((1, 5,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1,)) == t12
        assert t12.select_sub_tree_from_path_sequence((1, 1,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 2,)) == t2_a_aa
        assert t12.select_sub_tree_from_path_sequence((1, 2, 1,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 3,)) == t6_a_aa_ab_ac_ad_ae
        assert t12.select_sub_tree_from_path_sequence((1, 3, 1,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 3, 2,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 3, 3,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 3, 4,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 3, 5,)) == t1_a
        assert t12.select_sub_tree_from_path_sequence((1, 4,)) == t2_a_aa
        assert t12.select_sub_tree_from_path_sequence((1, 4, 1,)) == t1_a

    def test_tuple_tree_constructor(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        t1b = pu.rptl.RootedPlaneTree.from_tuple_tree(())
        assert t1b == t1_a
        t2b = pu.rptl.RootedPlaneTree.from_tuple_tree(((),))
        assert t2b == t2_a_aa
        t3b = pu.rptl.RootedPlaneTree.from_tuple_tree(((), (), (), (), (),))
        assert t3b == t6_a_aa_ab_ac_ad_ae
        t4b = pu.rptl.RootedPlaneTree.from_tuple_tree(((), ((),), ((), (), (), (), (),), ((),),))
        assert t4b == t12

    def test_iterate_direct_ascending(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        l = tuple(t for t in t1_a.iterate_immediate_subtrees())
        assert len(l) == 0
        l = tuple(t for t in t2_a_aa.iterate_immediate_subtrees())
        assert l[0] == t1_a
        l = tuple(t for t in t6_a_aa_ab_ac_ad_ae.iterate_immediate_subtrees())
        assert l[0] == t1_a
        assert l[1] == t1_a
        assert l[2] == t1_a
        assert l[3] == t1_a
        assert l[4] == t1_a
        l = tuple(t for t in t12.iterate_immediate_subtrees())
        assert l[0] == t1_a
        assert l[1] == t2_a_aa
        assert l[2] == t6_a_aa_ab_ac_ad_ae
        assert l[3] == t2_a_aa

    def test_iterate_depth_first_ascending(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        l = tuple(t for t in t1_a.iterate_subtrees())
        assert l[0] == t1_a
        l = tuple(t for t in t2_a_aa.iterate_subtrees())
        assert l[0] == t2_a_aa
        assert l[1] == t1_a
        l = tuple(t for t in t6_a_aa_ab_ac_ad_ae.iterate_subtrees())
        assert l[0] == t6_a_aa_ab_ac_ad_ae
        assert l[1] == t1_a
        assert l[2] == t1_a
        assert l[3] == t1_a
        assert l[4] == t1_a
        assert l[5] == t1_a
        l = tuple(t for t in t12.iterate_subtrees())
        assert l[0] == t12
        assert l[1] == t1_a
        assert l[2] == t2_a_aa
        assert l[3] == t1_a
        assert l[4] == t6_a_aa_ab_ac_ad_ae
        assert l[5] == t1_a
        assert l[6] == t1_a
        assert l[7] == t1_a
        assert l[8] == t1_a
        assert l[9] == t1_a
        assert l[10] == t2_a_aa
        assert l[11] == t1_a

    def test_get_sub_tree_by_path(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12, t_big):
        assert t1_a.get_subtree_by_path((0,)) == t1_a
        assert t2_a_aa.get_subtree_by_path((0,)) == t2_a_aa
        assert t2_a_aa.get_subtree_by_path((0, 0,)) == t1_a
        assert t_big.get_subtree_by_path((0, 3,)) == t12
        assert t_big.get_subtree_by_path((0, 3, 2,)) == t6_a_aa_ab_ac_ad_ae
        assert t_big.get_subtree_by_path((0, 3, 2, 4,)) == t1_a

    def test_build_rooted_plane_tree_from_tuple_tree(self, t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
        u1 = pu.rptl.RootedPlaneTree.from_tuple_tree(())
        assert u1 == t1_a
        u1 = pu.rptl.RootedPlaneTree.from_tuple_tree(((),))
        assert u1 == t2_a_aa
        u1 = pu.rptl.RootedPlaneTree.from_tuple_tree(((), (), (), (), (),))
        assert u1 == t6_a_aa_ab_ac_ad_ae
        u1 = pu.rptl.RootedPlaneTree.from_tuple_tree(((), ((),), ((), (), (), (), (),), ((),),))
        assert u1 == t12

    def test_is_increasing(self, t1_a, t2_a_aa, t3_a_aa_aaa, t3_a_aa_ab, t6_a_aa_ab_ac_ad_ae,
                           t7_a_aa_ab_aaa_aaaa_aba_abaa,
                           t12, t_big):
        assert t1_a.is_increasing
        assert t2_a_aa.is_increasing
        assert t3_a_aa_aaa.is_increasing
        assert t3_a_aa_ab.is_increasing
        assert t6_a_aa_ab_ac_ad_ae.is_increasing
        assert t7_a_aa_ab_aaa_aaaa_aba_abaa.is_increasing
        assert not t12.is_increasing
        assert not t_big.is_increasing

    def test_is_strictly_increasing(self, t1_a, t2_a_aa, t3_a_aa_aaa, t3_a_aa_ab, t6_a_aa_ab_ac_ad_ae,
                                    t7_a_aa_ab_aaa_aaaa_aba_abaa,
                                    t12, t_big):
        assert t1_a.is_strictly_increasing
        assert t2_a_aa.is_strictly_increasing
        assert t3_a_aa_aaa.is_strictly_increasing
        assert not t3_a_aa_ab.is_strictly_increasing
        assert not t6_a_aa_ab_ac_ad_ae.is_strictly_increasing
        assert not t7_a_aa_ab_aaa_aaaa_aba_abaa.is_strictly_increasing
        assert not t12.is_strictly_increasing
        assert not t_big.is_strictly_increasing

    def test_consistency_of_rpt_generation_with_catalan_numbers(self):
        """The number of unique RPTs per size (in vertices) must be equal to the Catalan numbers.

        :return:
        """
        tree_statistics = []
        size_statistics = []

        current_tree = pu.rptl.RootedPlaneTree()
        current_tree_size = 0

        current_size_counter = 1
        expected_catalan_number = 0
        previous_tree_size = 1
        tree_statistics.append(f"0: {current_tree.size}: {current_tree.dyck_word}")
        for i in range(1, 1024):
            current_tree: pu.rptl.RootedPlaneTree = current_tree.successor()
            # Size cannot decrease
            assert current_tree.size >= current_tree_size
            if current_tree.size > current_tree_size:
                # Everytime we move to a new size, the number of trees in the precedent size group
                # must be equal to the corresponding Catalan number.
                assert current_size_counter == pu.catalan_number_library.get_catalan_number(expected_catalan_number)
                size_statistics.append(f"INCREASE: size={current_tree_size}, counter={current_size_counter}")
                # size increase
                expected_catalan_number += 1
                current_tree_size = current_tree.size
                current_size_counter = 1
            else:
                current_size_counter += 1
        pass

        # for n in range(1, 10):
        #    assert len(pu.rptc.RootedPlaneTreeGenerator.get_ordered_set_of_rooted_plane_trees_of_size_n(
        #        n)) == pu.catalan_number_library.get_catalan_number(n - 1)

    def test_dyck_word_lexicographic_order(self):
        for n in range(0, 100):
            t1 = pu.rptl.dyck_word_lexicographic_order.unrank(n)
            d1 = pu.dwl.lexicographic_order.unrank(n)
            assert t1.dyck_word == d1
            d2 = t1.dyck_word
            assert d1 == d2
            n2 = pu.rptl.dyck_word_lexicographic_order.rank(t1)
            assert n2 == n
            n3 = pu.dwl.lexicographic_order.rank(d1)
            assert n3 == n2

    def test_least_element(self):
        assert pu.rptl.DyckWordLexicographicOrder.least_element == pu.rptl.RPT()
        assert pu.rptl.RPT.least_element == pu.rptl.RPT()
