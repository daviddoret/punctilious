import itertools
import punctilious.util as util
import punctilious.natural_number_sequence_library as sl


class NaturalNumberSequenceGenerator:
    _ordered_set_of_trees_grouped_by_size = ()  # A tuple of tuples of RPTs, where _rpt_database[i] gives the list of RPTs of size i + 1

    @classmethod
    def get_ordered_set_of_natural_number_sequences_of_size_n(cls, n: int) -> tuple[sl.NaturalNumberSequence, ...]:
        """

        :param n: the size of the trees.
        :return: the ordered set of all natural-number-sequences of size `n` by canonical order.
        """
        if len(NaturalNumberSequenceGenerator._ordered_set_of_trees_grouped_by_size) < n:
            # the database does not contain the natural-number-sequence of that size,
            # generate them and store them in the database.
            for missing_tree_size in range(
                    len(NaturalNumberSequenceGenerator._ordered_set_of_trees_grouped_by_size) + 1,
                    n + 1):
                NaturalNumberSequenceGenerator._generate_ordered_set_of_natural_number_sequences_of_size_n(
                    missing_tree_size)
        j = n - 1
        return NaturalNumberSequenceGenerator._ordered_set_of_trees_grouped_by_size[j]

    @classmethod
    def _generate_ordered_set_of_natural_number_sequences_of_size_n(cls, n: int):
        if n < 1:
            raise util.PunctiliousException("Invalid parameter", n=n)
        if n == 1:
            leaf = sl.NaturalNumberSequence()
            NaturalNumberSequenceGenerator._ordered_set_of_trees_grouped_by_size = ((leaf,),)
        else:
            subtree_sizes_combinations = tuple(sl.get_sequences_of_natural_numbers_whose_sum_equals_n(n - 1))
            ordered_set_of_trees_of_size_n = ()
            for subtree_sizes in subtree_sizes_combinations:

                l = []
                for n in subtree_sizes:
                    l.append(NaturalNumberSequenceGenerator.get_ordered_set_of_natural_number_sequences_of_size_n(n))

                for s in itertools.product(*l):
                    subtree: sl.NaturalNumberSequence = sl.NaturalNumberSequence(*s)
                    ordered_set_of_trees_of_size_n = ordered_set_of_trees_of_size_n + (subtree,)
            NaturalNumberSequenceGenerator._ordered_set_of_trees_grouped_by_size = NaturalNumberSequenceGenerator._ordered_set_of_trees_grouped_by_size + (
                ordered_set_of_trees_of_size_n,)


s0 = sl.NaturalNumberSequence(0, )  # ( 0 )
s0_0 = sl.NaturalNumberSequence(0, 0, )  # ( 0, 0 )
s0_1 = sl.NaturalNumberSequence(0, 1, )  # ( 0, 1 )

pass
