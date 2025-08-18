import punctilious as pu


class TestAbstractOrderedSet:

    def test_abstract_ordered_set(self):
        # declare ordered set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.AbstractOrderedSet(t0_123)
        assert s123.cardinality == 3
        assert not s123.has_element(t0_123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_abstract_ordered_set_equivalent_to(s123)

        # confirm order matters
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.AbstractOrderedSet(t0_321)
        assert s321.cardinality == 3
        assert not s321.has_element(t0_123)
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
        s333221212 = pu.ssl.AbstractOrderedSet(t0_333221212)
        assert s333221212.cardinality == 3
        assert not s333221212.has_element(t0_123)
        assert not s333221212.has_element(t0)
        assert s333221212.has_element(t1)
        assert s333221212.has_element(t2)
        assert s333221212.has_element(t3)
        assert not s333221212.has_element(t4)
        assert s333221212.is_abstract_ordered_set_equivalent_to(s333221212)

        assert not s123.is_abstract_ordered_set_equivalent_to(s333221212)
        assert s321.is_abstract_ordered_set_equivalent_to(s333221212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.AbstractOrderedSet(t0_12)
        assert not s123.is_abstract_ordered_set_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.AbstractOrderedSet(t0)
        assert not s123.is_abstract_ordered_set_equivalent_to(s_empty)
        assert s_empty.cardinality == 0


class TestAbstractSet:

    def test_abstract_set(self):
        # declare set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.AbstractSet(t0_123)
        assert s123.cardinality == 3
        assert not s123.has_element(t0_123)
        assert not s123.has_element(t0)
        assert s123.has_element(t1)
        assert s123.has_element(t2)
        assert s123.has_element(t3)
        assert not s123.has_element(t4)
        assert s123.is_abstract_set_equivalent_to(s123)

        # confirm order does not matter
        t0_321 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (3, 2, 1,)))
        s321 = pu.ssl.AbstractSet(t0_321)
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
        s3331212 = pu.ssl.AbstractSet(t0_3331212)
        assert s3331212.cardinality == 3
        assert not s3331212.has_element(t0_123)
        assert not s3331212.has_element(t0)
        assert s3331212.has_element(t1)
        assert s3331212.has_element(t2)
        assert s3331212.has_element(t3)
        assert not s3331212.has_element(t4)
        assert s3331212.is_abstract_set_equivalent_to(s3331212)

        assert s123.is_abstract_set_equivalent_to(s3331212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.AbstractSet(t0_12)
        assert not s123.is_abstract_set_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.AbstractSet(t0)
        assert not s123.is_abstract_set_equivalent_to(s_empty)
        assert s_empty.cardinality == 0


class TestAbstractTuple:

    def test_abstract_tuple(self):
        # declare set {1, 2, 3}
        t0_123 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2, 3,)))
        t0 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(0)
        t1 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(1)
        t2 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(2)
        t3 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(3)
        t4 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs(4)
        s123 = pu.ssl.AbstractTuple(t0_123)
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
        s321 = pu.ssl.AbstractTuple(t0_321)
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
        s3331212 = pu.ssl.AbstractTuple(t0_3331212)
        assert s3331212.cardinality == 7
        assert not s3331212.has_element(t0_123)
        assert not s3331212.has_element(t0)
        assert s3331212.has_element(t1)
        assert s3331212.has_element(t2)
        assert s3331212.has_element(t3)
        assert not s3331212.has_element(t4)
        assert s3331212.is_abstract_tuple_equivalent_to(s3331212)

        assert not s321.is_abstract_tuple_equivalent_to(s3331212)

        t0_12 = pu.lrptl.LabeledRootedPlaneTree.from_tree_of_integer_tuple_pairs((0, (1, 2,)))
        s12 = pu.ssl.AbstractTuple(t0_12)
        assert not s123.is_abstract_tuple_equivalent_to(s12)
        assert s12.cardinality == 2

        s_empty = pu.ssl.AbstractTuple(t0)
        assert not s123.is_abstract_tuple_equivalent_to(s_empty)
        assert s_empty.cardinality == 0
