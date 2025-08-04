import pytest

import punctilious as pu


class TestAbstractSet:
    def test_abstract_set(self):
        s1 = pu.lrptl.LabeledRootedPlaneTree(t=((), (), (),), s=(0, 1, 2, 3,))
        s2 = pu.lrptl.LabeledRootedPlaneTree(t=((), (),), s=(0, 5, 2,))
        s3 = pu.lrptl.LabeledRootedPlaneTree(t=((), (), (), (), (),), s=(0, 1, 1, 1, 6, 1,))
        s4 = pu.lrptl.LabeledRootedPlaneTree.from_immediate_subtrees(0, (s1, s2, s3,))

        assert not pu.lrptl.LabeledRootedPlaneTree(t=(), s=(0,)).is_abstract_set_element_of(s1)
        assert pu.lrptl.LabeledRootedPlaneTree(t=(), s=(1,)).is_abstract_set_element_of(s1)

        assert not s1.has_abstract_set_element(pu.lrptl.LabeledRootedPlaneTree(t=(), s=(0,)))
        assert s1.has_abstract_set_element(pu.lrptl.LabeledRootedPlaneTree(t=(), s=(1,)))

        assert s1.is_abstract_set_element_of(s4)
        assert s2.is_abstract_set_element_of(s4)
        assert s3.is_abstract_set_element_of(s4)
        assert not s4.is_abstract_set_element_of(s4)

        assert s4.has_abstract_set_element(s1)
        assert s4.has_abstract_set_element(s2)
        assert s4.has_abstract_set_element(s3)
        assert not s4.has_abstract_set_element(s4)

        assert s1.abstract_set_elements == s1.immediate_subtrees
        assert s4.abstract_set_elements == s4.immediate_subtrees

        assert s3.canonical_abstract_set == pu.lrptl.LabeledRootedPlaneTree(t=((), (),), s=(0, 1, 6,))

        pass
