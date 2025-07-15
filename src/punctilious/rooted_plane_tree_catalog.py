import itertools
import punctilious.util as util
import punctilious.natural_number_1_sequence_library as nnsl
import punctilious.rooted_plane_tree_library as rptl


class RootedPlaneTreeGenerator:
    _ordered_set_of_trees_grouped_by_size = ()  # A tuple of tuples of RPTs, where _rpt_database[i] gives the list of RPTs of size i + 1

    @classmethod
    def get_ordered_set_of_rooted_plane_trees_of_size_n(cls, n: int) -> tuple[rptl.RootedPlaneTree, ...]:
        """

        :param n: the size of the trees.
        :return: the ordered set of all rooted-plane-trees of size `n` by canonical order.
        """
        if len(RootedPlaneTreeGenerator._ordered_set_of_trees_grouped_by_size) < n:
            # the database does not contain the rooted-plane-tree of that size,
            # generate them and store them in the database.
            for missing_tree_size in range(len(RootedPlaneTreeGenerator._ordered_set_of_trees_grouped_by_size) + 1,
                                           n + 1):
                RootedPlaneTreeGenerator._generate_ordered_set_of_rooted_plane_trees_of_size_n(missing_tree_size)
        j = n - 1
        return RootedPlaneTreeGenerator._ordered_set_of_trees_grouped_by_size[j]

    @classmethod
    def _generate_ordered_set_of_rooted_plane_trees_of_size_n(cls, n: int):
        if n < 1:
            raise util.PunctiliousException("Invalid parameter", n=n)
        if n == 1:
            leaf = rptl.RootedPlaneTree()
            RootedPlaneTreeGenerator._ordered_set_of_trees_grouped_by_size = ((leaf,),)
        else:
            # subtree_sizes_combinations = tuple(nnsl.get_sequences_of_natural_numbers_whose_sum_equals_n(n - 1))
            subtree_sizes_combinations = tuple(
                nnsl.NaturalNumber1Sequence.get_o1_ordered_set_of_natural_number_sequences_of_sum_n(n - 1))
            ordered_set_of_trees_of_size_n = ()
            for subtree_sizes in subtree_sizes_combinations:

                l = []
                for n in subtree_sizes:
                    l.append(RootedPlaneTreeGenerator.get_ordered_set_of_rooted_plane_trees_of_size_n(n))

                for s in itertools.product(*l):
                    subtree: rptl.RootedPlaneTree = rptl.RootedPlaneTree(*s)
                    if subtree not in ordered_set_of_trees_of_size_n:
                        ordered_set_of_trees_of_size_n = ordered_set_of_trees_of_size_n + (subtree,)
            RootedPlaneTreeGenerator._ordered_set_of_trees_grouped_by_size = RootedPlaneTreeGenerator._ordered_set_of_trees_grouped_by_size + (
                ordered_set_of_trees_of_size_n,)


# 1-node trees

#: ⬤
leaf = rptl.RootedPlaneTree()

#: ⬤
t1_a = leaf

# 2-nodes trees

#: ⬤━━━⬤
t2_a_aa = rptl.RootedPlaneTree(leaf)

# 3-nodes trees

#: ⬤━━━⬤━━━⬤
t3_a_aa_aaa = rptl.RootedPlaneTree(t2_a_aa)

#: ⬤━┳━⬤
#:   ┗━⬤
t3_a_aa_ab = rptl.RootedPlaneTree(leaf, leaf)

# 4-nodes trees

#: ⬤━━━⬤━━━⬤━━━⬤
t4_a_aa_aaa_aaaa = rptl.RootedPlaneTree(t3_a_aa_aaa)

#: ⬤━━━⬤━┳━⬤
#:       ┗━⬤
t4_a_aa_aaa_aab = rptl.RootedPlaneTree(t3_a_aa_ab)

#: ⬤━┳━⬤━━━⬤
#:   ┗━⬤
t4_a_aa_aaa_ab = rptl.RootedPlaneTree(t2_a_aa, leaf)

#: ⬤━┳━⬤
#:   ┗━⬤━━━⬤
t4_a_aa_ab_aba = rptl.RootedPlaneTree(leaf, t2_a_aa)

#: ⬤━┳━⬤
#:   ┣━⬤
#:   ┗━⬤
t4_a_aa_ab_ac = rptl.RootedPlaneTree(leaf, leaf, leaf)

# 5 nodes trees
t5_a_aa_aaa_aaaa_aaaaa = rptl.RootedPlaneTree(t4_a_aa_aaa_aaaa)
# there must be 14 trees in this section


pass
