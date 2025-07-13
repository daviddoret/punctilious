import itertools
import punctilious.util as util
import punctilious.natural_number_sequence_library as sl


class NaturalNumberSequenceGeneratorUnderO1:
    _ordered_set_of_sequence_grouped_by_sum = ()  # A tuple of tuples of RPTs, where _rpt_database[i] gives the list of RPTs of size i + 1

    @classmethod
    def get_ordered_set_of_natural_number_sequences_of_sum_n(cls, n: int) -> tuple[sl.NaturalNumberSequence, ...]:
        if len(NaturalNumberSequenceGeneratorUnderO1._ordered_set_of_sequence_grouped_by_sum) < n:
            # the database does not contain the natural-number-sequence of that size,
            # generate them and store them in the database.
            for missing_tree_size in range(
                    len(NaturalNumberSequenceGeneratorUnderO1._ordered_set_of_sequence_grouped_by_sum) + 1,
                    n + 1):
                NaturalNumberSequenceGeneratorUnderO1._generate_ordered_set_of_natural_number_sequences_of_sum_n(
                    missing_tree_size)
        j = n - 1
        return NaturalNumberSequenceGeneratorUnderO1._ordered_set_of_sequence_grouped_by_sum[j]

    @classmethod
    def _generate_ordered_set_of_natural_number_sequences_of_sum_n(cls, n: int):
        if n < 1:
            raise util.PunctiliousException("Invalid parameter", n=n)
        if n == 1:
            strictly_minimal_element = sl.NaturalNumberSequence(1)
            NaturalNumberSequenceGeneratorUnderO1._ordered_set_of_sequence_grouped_by_sum = (
                (strictly_minimal_element,),)
        else:
            sequence_combinations = tuple(sl.get_sequences_of_natural_numbers_whose_sum_equals_n(n - 1))
            ordered_set_of_natural_number_sequence_of_sum_n = ()
            for s in sequence_combinations:
                for i in range(len(s)):
                    modified = s[:i] + (s[i] + 1,) + s[i + 1:]
                    modified = sl.NaturalNumberSequence(*modified)
                    if modified not in ordered_set_of_natural_number_sequence_of_sum_n:
                        # a more optimal algorithm is probably possible,
                        # avoiding the "not in" check.
                        ordered_set_of_natural_number_sequence_of_sum_n += (modified,)
                extended = s + (1,)
                extended = sl.NaturalNumberSequence(*extended)
                if extended not in ordered_set_of_natural_number_sequence_of_sum_n:
                    # a more optimal algorithm is probably possible,
                    # avoiding the "not in" check.
                    ordered_set_of_natural_number_sequence_of_sum_n += (extended,)

            NaturalNumberSequenceGeneratorUnderO1._ordered_set_of_sequence_grouped_by_sum = NaturalNumberSequenceGeneratorUnderO1._ordered_set_of_sequence_grouped_by_sum + (
                ordered_set_of_natural_number_sequence_of_sum_n,)


pass
