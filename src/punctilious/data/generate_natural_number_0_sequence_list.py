import csv
import punctilious as pu

# Define the CSV file name
filename = "natural_number_0_sequence_list.csv"
list_size = 4096

# Define the header and some sample data
header = ["Rank", "Sequence", "Rank as bits", "Sum", "Adjusted sum", "Length", "Rank in adjusted sum and length class",
          "Image cardinality", "Image",
          "Is strictly increasing",
          "Is RGF sequence"]
data = []

# Writing to the CSV file with pipe separator
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="|")
    csvwriter.writerow(header)
    for rank in range(list_size):
        if rank == 0:
            s: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.NaturalNumber0Sequence.least_element
        else:
            # s: pu.nn0sl.NaturalNumber0Sequence = s.successor()
            s: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.AdjustedSumFirstLengthSecondReverseLexicographicThirdOrder.successor(
                s)
        record = [rank,
                  s,
                  pu.util.int_to_bits(rank),
                  s.sum,
                  pu.nn0sl.get_adjusted_sum(s),
                  s.length,
                  pu.nn0sl.get_reverse_lexicographic_rank_within_adjusted_sum_and_length_class(s),
                  s.image_cardinality,
                  s.image, s.is_strictly_increasing,
                  s.is_restricted_growth_function_sequence]
        csvwriter.writerow(record)
