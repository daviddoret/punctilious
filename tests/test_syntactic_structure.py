import punctilious as pu


class TestSyntacticStructure:
    def test_syntactic_structure(self):
        lrpt1 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        ss1 = pu.ssl.SyntacticStructure.from_lrpt(lrpt1)
        ss2 = pu.ssl.SyntacticStructure(rpt=ss1.rooted_plane_tree, sequence=ss1.natural_number_sequence)
        assert ss1 == ss2
        pass

    def test_substitute(self):
        domain = pu.ssl.SyntacticOrderedSet.from_elements(1, 2, 3)
        codomain = pu.ssl.SyntacticTuple.from_elements(4, 5, 6)
        m1 = pu.ssl.SyntacticMap.from_domain_and_codomain(domain, codomain)
        input_1 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs(2)
        output_1 = m1.substitute(input_1)
        assert output_1 == pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs(5)
        output_2 = m1.substitute(output_1)
        assert output_2 == output_1
        input_3 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((0, (3, 9, 1)))
        output_3 = m1.substitute(input_3)
        assert output_3 == pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((0, (6, 9, 4)))

        ss1 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((0, (1, 2)))
        ss2a = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((1, (2,)))
        ss2 = pu.ssl.SyntacticStructure.from_immediate_subtrees(ss2a, n=0)
        ss3 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((4, (5,)))
        ss4 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((7, (8, 8, 8,)))
        domain2 = pu.ssl.SyntacticOrderedSet.from_elements(ss1, ss2)
        codomain2 = pu.ssl.SyntacticTuple.from_elements(ss3, ss4)
        m2 = pu.ssl.SyntacticMap.from_domain_and_codomain(domain2, codomain2)
        input_4 = pu.ssl.SyntacticStructure.from_immediate_subtrees(ss1, n=5)
        output_4 = m2.substitute(input_4)
        assert output_4 == pu.ssl.SyntacticStructure.from_immediate_subtrees(ss3, n=5)
        input_5 = pu.ssl.SyntacticStructure.from_immediate_subtrees(ss3, ss1, ss2, ss3, n=9)
        output_5 = m2.substitute(input_5)
        assert output_5 == pu.ssl.SyntacticStructure.from_immediate_subtrees(ss3, ss3, ss4, ss3, n=9)
        pass


class TestSyntacticOrderedSet:

    def test_syntactic_ordered_set(self):
        # declare ordered set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.SyntacticOrderedSet.from_elements(t1, t2, t3, )
        assert s123.is_labeled_rooted_plane_tree_equivalent_to(s123)
        assert s123.cardinality == 3
        assert not s123.has_element(s123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_syntactic_ordered_set_equivalent_to(s123)

        # confirm order matters
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.SyntacticOrderedSet.from_elements(t3, t2, t1)
        assert s321.is_labeled_rooted_plane_tree_equivalent_to(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(s321)
        assert not s321.has_element(t0)
        assert s321.has_element(t1)
        assert s321.has_element(t2)
        assert s321.has_element(t3)
        assert not s321.has_element(t4)
        assert s321.is_syntactic_ordered_set_equivalent_to(s321)

        assert not s123.is_syntactic_ordered_set_equivalent_to(s321)

        # confirm duplicates do not matter
        t0_333221212 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(
            (0, (3, 3, 3, 2, 2, 1, 2, 1, 2,)))
        s333221212 = pu.ssl.SyntacticOrderedSet.from_elements(t3, t3, t3, t2, t2, t1, t2, t1, t2)
        assert s333221212.is_labeled_rooted_plane_tree_equivalent_to(t0_333221212)
        assert s333221212.cardinality == 3
        assert not s333221212.has_element(s333221212)
        assert not s333221212.has_element(t0)
        assert s333221212.has_element(t1)
        assert s333221212.has_element(t2)
        assert s333221212.has_element(t3)
        assert not s333221212.has_element(t4)
        assert s333221212.is_syntactic_ordered_set_equivalent_to(s333221212)

        assert not s123.is_syntactic_ordered_set_equivalent_to(s333221212)
        assert s321.is_syntactic_ordered_set_equivalent_to(s333221212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.SyntacticOrderedSet.from_lrpt(t0_12)
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert not s123.is_syntactic_ordered_set_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.SyntacticOrderedSet.from_lrpt(t0)
        assert not s123.is_syntactic_ordered_set_equivalent_to(s_empty)
        assert s_empty.cardinality == 0

        pass


class TestSyntacticSet:

    def test_syntactic_set(self):
        # declare set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.SyntacticSet.from_elements(t1, t2, t3)
        assert s123.is_labeled_rooted_plane_tree_equivalent_to(t0_123)
        assert s123.cardinality == 3
        assert not s123.has_element(s123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_syntactic_set_equivalent_to(s123)

        # confirm order does not matter
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.SyntacticSet.from_elements(t3, t2, t1)
        assert s321.is_labeled_rooted_plane_tree_equivalent_to(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(t0_123)
        assert not s321.has_element(t0)
        assert s321.has_element(t1)
        assert s321.has_element(t2)
        assert s321.has_element(t3)
        assert not s321.has_element(t4)
        assert s321.is_syntactic_set_equivalent_to(s321)

        assert s123.is_syntactic_set_equivalent_to(s321)

        # confirm duplicates do not matter
        t0_3331212 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 3, 3, 1, 2, 1, 2,)))
        s3331212 = pu.ssl.SyntacticSet.from_elements(t3, t3, t3, t1, t2, t1, t2)
        assert s3331212.is_labeled_rooted_plane_tree_equivalent_to(t0_3331212)
        assert s3331212.cardinality == 3
        assert not s3331212.has_element(s3331212)
        assert not s3331212.has_element(t0)
        assert s3331212.has_element(t1)
        assert s3331212.has_element(t2)
        assert s3331212.has_element(t3)
        assert not s3331212.has_element(t4)
        assert s3331212.is_syntactic_set_equivalent_to(s3331212)

        assert s123.is_syntactic_set_equivalent_to(s3331212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.SyntacticSet.from_elements(t1, t2)
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert not s123.is_syntactic_set_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.SyntacticSet.from_lrpt(t0)
        assert not s123.is_syntactic_set_equivalent_to(s_empty)
        assert s_empty.cardinality == 0

        pass

    def test_empty_set(self):
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        assert s0 == pu.ssl.SyntacticSet.from_empty_set()
        assert s0.cardinality == 0

    def test_append(self):
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        s0 = s0.append(t0)
        assert s0.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t0))
        assert s0.cardinality == 1
        s0 = s0.append(t1)
        assert s0.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t1, t0))
        assert s0.cardinality == 2
        s0 = s0.append(t1)
        assert s0.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t0, t1))
        assert s0.cardinality == 2
        s0 = s0.append(t2)
        assert s0.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t1, t2, t0))
        assert s0.cardinality == 3

    def test_union(self):
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        s1 = s0.union(s0)
        assert s1.is_syntactic_set_equivalent_to(s0)
        s2 = pu.ssl.SyntacticSet.from_elements(t0)
        s3 = s1.union(s2)
        assert s3.is_syntactic_set_equivalent_to(s2)
        s4 = pu.ssl.SyntacticSet.from_elements(t0, t3, t2)
        s5 = s3.union(s4)
        assert s5.is_syntactic_set_equivalent_to(s4)
        s6 = pu.ssl.SyntacticSet.from_elements(t4, t4, t2, t3)
        s6 = s6.union(s5)
        s7 = pu.ssl.SyntacticSet.from_elements(t4, t2, t3, t0)
        assert s6.is_syntactic_set_equivalent_to(s7)

    def test_intersection(self):
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        s1 = pu.ssl.SyntacticSet.from_elements(t0, t1, t2)
        s2 = pu.ssl.SyntacticSet.from_elements(t4, t2, t3)
        s3 = s1.intersection(s2)
        assert s3.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t2))
        s4 = s1.intersection(s0)
        assert s4.is_syntactic_set_equivalent_to(s0)
        assert s3.intersection(s3).is_syntactic_set_equivalent_to(s3)
        assert s4.intersection(s4).is_syntactic_set_equivalent_to(s4)

    def test_difference(self):
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        s1 = pu.ssl.SyntacticSet.from_elements(t0, t1, t2)
        s2 = pu.ssl.SyntacticSet.from_elements(t4, t2, t3)
        s3 = s1.difference(s2)
        assert s3.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t0, t1))
        s4 = s1.difference(s0)
        assert s4.is_syntactic_set_equivalent_to(s1)
        assert s3.difference(s3).is_syntactic_set_equivalent_to(s0)
        assert s4.difference(s4).is_syntactic_set_equivalent_to(s0)

    def test_symmetric_difference(self):
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        s1 = pu.ssl.SyntacticSet.from_elements(t0, t1, t2)
        s2 = pu.ssl.SyntacticSet.from_elements(t4, t2, t3)
        s3 = s1.symmetric_difference(s2)
        assert s3.is_syntactic_set_equivalent_to(pu.ssl.SyntacticSet.from_elements(t0, t1, t3, t4))
        s4 = s1.symmetric_difference(s0)
        assert s4.is_syntactic_set_equivalent_to(s4)
        assert s3.symmetric_difference(s3).is_syntactic_set_equivalent_to(s0)
        assert s4.symmetric_difference(s4).is_syntactic_set_equivalent_to(s0)

    def test_cartesian_produc(self):
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s0 = pu.ssl.SyntacticSet.from_empty_set()
        s1 = pu.ssl.SyntacticSet.from_elements(t0, t1, t2)
        s2 = pu.ssl.SyntacticSet.from_elements(t3, t4)
        s3 = s1.cartesian_product(s2)
        assert s3.has_element(pu.ssl.SyntacticOrderedPair.from_first_and_second_elements(t0, t3))
        assert s3.has_element(pu.ssl.SyntacticOrderedPair.from_first_and_second_elements(t0, 4))
        assert s3.has_element(pu.ssl.SyntacticOrderedPair.from_first_and_second_elements(t1, t3))
        assert s3.has_element(pu.ssl.SyntacticOrderedPair.from_first_and_second_elements(t1, t4))
        assert s3.has_element(pu.ssl.SyntacticOrderedPair.from_first_and_second_elements(t2, t3))
        assert s3.has_element(pu.ssl.SyntacticOrderedPair.from_first_and_second_elements(t2, t4))
        s4 = s1.cartesian_product(s0)
        assert s4.is_syntactic_set_equivalent_to(s0)


class TestSyntacticTuple:

    def test_syntactic_tuple(self):
        # declare set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s123 = pu.ssl.SyntacticTuple.from_elements(t1, t2, t3)
        assert s123.is_labeled_rooted_plane_tree_equivalent_to(t0_123)
        assert s123.cardinality == 3
        assert not s123.has_element(t0_123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_syntactic_tuple_equivalent_to(s123)

        # confirm order does matter
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.SyntacticTuple.from_elements(t3, t2, t1)
        assert s321.is_labeled_rooted_plane_tree_equivalent_to(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(t0_123)
        assert not s321.has_element(t0)
        assert s321.has_element(t1)
        assert s321.has_element(t2)
        assert s321.has_element(t3)
        assert not s321.has_element(t4)
        assert s321.is_syntactic_tuple_equivalent_to(s321)

        assert not s123.is_syntactic_tuple_equivalent_to(s321)

        # confirm duplicates matter
        t0_3331212 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 3, 3, 1, 2, 1, 2,)))
        s3331212 = pu.ssl.SyntacticTuple.from_elements(t3, t3, t3, t1, t2, t1, t2)
        assert s3331212.is_labeled_rooted_plane_tree_equivalent_to(t0_3331212)
        assert s3331212.cardinality == 7
        assert not s3331212.has_element(s3331212)
        assert not s3331212.has_element(t0)
        assert s3331212.has_element(t1)
        assert s3331212.has_element(t2)
        assert s3331212.has_element(t3)
        assert not s3331212.has_element(t4)
        assert s3331212.is_syntactic_tuple_equivalent_to(s3331212)

        assert not s321.is_syntactic_tuple_equivalent_to(s3331212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.SyntacticTuple.from_elements(t1, t2)
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert not s123.is_syntactic_tuple_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.SyntacticTuple.from_lrpt(t0)
        assert not s123.is_syntactic_tuple_equivalent_to(s_empty)
        assert s_empty.cardinality == 0

        pass


class TestSyntacticOrderedPair:

    def test_syntactic_ordered_pair(self):
        # declare set {1, 2, 3}
        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        t0 = pu.ssl.SyntacticStructure.from_integer(0)
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        s12 = pu.ssl.SyntacticOrderedPair.from_elements(t1, t2, )
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert s12.first_element == t1
        assert s12.second_element == t2
        assert s12.cardinality == 2
        assert not s12.has_element(t0_12)
        assert not s12.has_element(t0)
        assert s12.has_element(t1)
        assert s12.has_element(t2)
        assert not s12.has_element(t4)
        assert s12.is_syntactic_tuple_equivalent_to(s12)

        # confirm order does matter
        t0_21 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (2, 1,)))
        s21 = pu.ssl.SyntacticOrderedPair.from_elements(t2, t1)
        assert s21.is_labeled_rooted_plane_tree_equivalent_to(t0_21)
        assert s21.first_element == t2
        assert s21.second_element == t1
        assert s21.cardinality == 2
        assert not s21.has_element(t0_12)
        assert not s21.has_element(t0)
        assert s21.has_element(t1)
        assert s21.has_element(t2)
        assert not s21.has_element(t4)
        assert s21.is_syntactic_tuple_equivalent_to(s21)

        assert not s12.is_syntactic_tuple_equivalent_to(s21)

        pass


class TestSyntacticMap:

    def test_syntactic_map(self):
        # generate some basic elements to play with
        t1 = pu.ssl.SyntacticStructure.from_integer(1)
        t2 = pu.ssl.SyntacticStructure.from_integer(2)
        t3 = pu.ssl.SyntacticStructure.from_integer(3)
        t4 = pu.ssl.SyntacticStructure.from_integer(4)
        t5 = pu.ssl.SyntacticStructure.from_integer(5)
        domain = pu.ssl.SyntacticOrderedSet.from_elements(t3, t1, t4)
        codomain = pu.ssl.SyntacticTuple.from_elements(t5, t5, t1)
        m1 = pu.ssl.SyntacticMap.from_domain_and_codomain(domain, codomain)
        assert m1.get_value(t3) == t5
        assert m1.get_value(t1) == t5
        assert m1.get_value(t4) == t1
        assert not m1.has_domain_element(t2)
        pairs = m1.ordered_pairs
        assert pairs.degree == 3
