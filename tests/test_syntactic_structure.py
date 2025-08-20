import punctilious as pu


class TestSyntacticStructure:
    def test_syntactic_structure(self):
        lrpt1 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        ss1 = pu.ssl.SyntacticStructure.from_lrpt(lrpt1)
        ss2 = pu.ssl.SyntacticStructure(rpt=ss1.rooted_plane_tree, sequence=ss1.natural_number_sequence)
        assert ss1 == ss2
        pass

    def test_substitute(self):
        domain = pu.ssl.AbstractOrderedSet.from_elements(1, 2, 3)
        codomain = pu.ssl.AbstractTuple.from_elements(4, 5, 6)
        m1 = pu.ssl.AbstractMap.from_domain_and_codomain(domain, codomain)
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
        ss2 = pu.ssl.SyntacticStructure.from_immediate_subtrees(0, (ss2a,))
        ss3 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((4, (5,)))
        ss4 = pu.ssl.SyntacticStructure.from_tree_of_integer_tuple_pairs((7, (8, 8, 8,)))
        domain2 = pu.ssl.AbstractOrderedSet.from_elements(ss1, ss2)
        codomain2 = pu.ssl.AbstractTuple.from_elements(ss3, ss4)
        m2 = pu.ssl.AbstractMap.from_domain_and_codomain(domain2, codomain2)
        input_4 = pu.ssl.SyntacticStructure.from_immediate_subtrees(5, (ss1,))
        output_4 = m2.substitute(input_4)
        assert output_4 == pu.ssl.SyntacticStructure.from_immediate_subtrees(5, (ss3,))
        input_5 = pu.ssl.SyntacticStructure.from_immediate_subtrees(9, (ss3, ss1, ss2, ss3))
        output_5 = m2.substitute(input_5)
        assert output_5 == pu.ssl.SyntacticStructure.from_immediate_subtrees(9, (ss3, ss3, ss4, ss3))
        pass


class TestAbstractOrderedSet:

    def test_abstract_ordered_set(self):
        # declare ordered set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.AbstractOrderedSet.from_elements(t1, t2, t3, )
        assert s123.is_labeled_rooted_plane_tree_equivalent_to(s123)
        assert s123.cardinality == 3
        assert not s123.has_element(s123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_abstract_ordered_set_equivalent_to(s123)

        # confirm order matters
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.AbstractOrderedSet.from_elements(t3, t2, t1)
        assert s321.is_labeled_rooted_plane_tree_equivalent_to(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(s321)
        assert not s321.has_element(t0)
        assert s321.has_element(t1)
        assert s321.has_element(t2)
        assert s321.has_element(t3)
        assert not s321.has_element(t4)
        assert s321.is_abstract_ordered_set_equivalent_to(s321)

        assert not s123.is_abstract_ordered_set_equivalent_to(s321)

        # confirm duplicates do not matter
        t0_333221212 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(
            (0, (3, 3, 3, 2, 2, 1, 2, 1, 2,)))
        s333221212 = pu.ssl.AbstractOrderedSet.from_elements(t3, t3, t3, t2, t2, t1, t2, t1, t2)
        assert s333221212.is_labeled_rooted_plane_tree_equivalent_to(t0_333221212)
        assert s333221212.cardinality == 3
        assert not s333221212.has_element(s333221212)
        assert not s333221212.has_element(t0)
        assert s333221212.has_element(t1)
        assert s333221212.has_element(t2)
        assert s333221212.has_element(t3)
        assert not s333221212.has_element(t4)
        assert s333221212.is_abstract_ordered_set_equivalent_to(s333221212)

        assert not s123.is_abstract_ordered_set_equivalent_to(s333221212)
        assert s321.is_abstract_ordered_set_equivalent_to(s333221212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.AbstractOrderedSet.from_lrpt(t0_12)
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert not s123.is_abstract_ordered_set_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.AbstractOrderedSet.from_lrpt(t0)
        assert not s123.is_abstract_ordered_set_equivalent_to(s_empty)
        assert s_empty.cardinality == 0

        pass


class TestAbstractSet:

    def test_abstract_set(self):
        # declare set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.AbstractSet.from_elements(t1, t2, t3)
        assert s123.is_labeled_rooted_plane_tree_equivalent_to(t0_123)
        assert s123.cardinality == 3
        assert not s123.has_element(s123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_abstract_set_equivalent_to(s123)

        # confirm order does not matter
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.AbstractSet.from_elements(t3, t2, t1)
        assert s321.is_labeled_rooted_plane_tree_equivalent_to(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(t0_123)
        assert not s321.has_element(t0)
        assert s321.has_element(t1)
        assert s321.has_element(t2)
        assert s321.has_element(t3)
        assert not s321.has_element(t4)
        assert s321.is_abstract_set_equivalent_to(s321)

        assert s123.is_abstract_set_equivalent_to(s321)

        # confirm duplicates do not matter
        t0_3331212 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 3, 3, 1, 2, 1, 2,)))
        s3331212 = pu.ssl.AbstractSet.from_elements(t3, t3, t3, t1, t2, t1, t2)
        assert s3331212.is_labeled_rooted_plane_tree_equivalent_to(t0_3331212)
        assert s3331212.cardinality == 3
        assert not s3331212.has_element(s3331212)
        assert not s3331212.has_element(t0)
        assert s3331212.has_element(t1)
        assert s3331212.has_element(t2)
        assert s3331212.has_element(t3)
        assert not s3331212.has_element(t4)
        assert s3331212.is_abstract_set_equivalent_to(s3331212)

        assert s123.is_abstract_set_equivalent_to(s3331212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.AbstractSet.from_elements(t1, t2)
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert not s123.is_abstract_set_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.AbstractSet.from_lrpt(t0)
        assert not s123.is_abstract_set_equivalent_to(s_empty)
        assert s_empty.cardinality == 0

        pass


class TestAbstractTuple:

    def test_abstract_tuple(self):
        # declare set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.AbstractTuple.from_elements(t1, t2, t3)
        assert s123.is_labeled_rooted_plane_tree_equivalent_to(t0_123)
        assert s123.cardinality == 3
        assert not s123.has_element(t0_123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_abstract_tuple_equivalent_to(s123)

        # confirm order does matter
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.AbstractTuple.from_elements(t3, t2, t1)
        assert s321.is_labeled_rooted_plane_tree_equivalent_to(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(t0_123)
        assert not s321.has_element(t0)
        assert s321.has_element(t1)
        assert s321.has_element(t2)
        assert s321.has_element(t3)
        assert not s321.has_element(t4)
        assert s321.is_abstract_tuple_equivalent_to(s321)

        assert not s123.is_abstract_tuple_equivalent_to(s321)

        # confirm duplicates matter
        t0_3331212 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 3, 3, 1, 2, 1, 2,)))
        s3331212 = pu.ssl.AbstractTuple.from_elements(t3, t3, t3, t1, t2, t1, t2)
        assert s3331212.is_labeled_rooted_plane_tree_equivalent_to(t0_3331212)
        assert s3331212.cardinality == 7
        assert not s3331212.has_element(s3331212)
        assert not s3331212.has_element(t0)
        assert s3331212.has_element(t1)
        assert s3331212.has_element(t2)
        assert s3331212.has_element(t3)
        assert not s3331212.has_element(t4)
        assert s3331212.is_abstract_tuple_equivalent_to(s3331212)

        assert not s321.is_abstract_tuple_equivalent_to(s3331212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.AbstractTuple.from_elements(t1, t2)
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert not s123.is_abstract_tuple_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.AbstractTuple.from_lrpt(t0)
        assert not s123.is_abstract_tuple_equivalent_to(s_empty)
        assert s_empty.cardinality == 0

        pass


class TestAbstractOrderedPair:

    def test_abstract_ordered_pair(self):
        # declare set {1, 2, 3}
        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s12 = pu.ssl.AbstractOrderedPair.from_elements(t1, t2, )
        assert s12.is_labeled_rooted_plane_tree_equivalent_to(t0_12)
        assert s12.first_element == t1
        assert s12.second_element == t2
        assert s12.cardinality == 2
        assert not s12.has_element(t0_12)
        assert not s12.has_element(t0)
        assert s12.has_element(t1)
        assert s12.has_element(t2)
        assert not s12.has_element(t4)
        assert s12.is_abstract_tuple_equivalent_to(s12)

        # confirm order does matter
        t0_21 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (2, 1,)))
        s21 = pu.ssl.AbstractOrderedPair.from_elements(t2, t1)
        assert s21.is_labeled_rooted_plane_tree_equivalent_to(t0_21)
        assert s21.first_element == t2
        assert s21.second_element == t1
        assert s21.cardinality == 2
        assert not s21.has_element(t0_12)
        assert not s21.has_element(t0)
        assert s21.has_element(t1)
        assert s21.has_element(t2)
        assert not s21.has_element(t4)
        assert s21.is_abstract_tuple_equivalent_to(s21)

        assert not s12.is_abstract_tuple_equivalent_to(s21)

        pass


class TestAbstractMap:

    def test_abstract_map(self):
        # generate some basic elements to play with
        t1 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs(4)
        t5 = pu.lrptl.LRPT.from_tree_of_integer_tuple_pairs(5)
        domain = pu.ssl.AbstractOrderedSet.from_elements(t3, t1, t4)
        codomain = pu.ssl.AbstractTuple.from_elements(t5, t5, t1)
        m1 = pu.ssl.AbstractMap.from_domain_and_codomain(domain, codomain)
        assert m1.get_value(t3) == t5
        assert m1.get_value(t1) == t5
        assert m1.get_value(t4) == t1
        assert not m1.has_domain_element(t2)
        pairs = m1.ordered_pairs
        assert pairs.degree == 3
