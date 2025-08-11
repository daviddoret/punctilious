import csv
import punctilious as pu

# Define the CSV file name
filename = "natural_number_0_sequence_list.csv"
list_size = 4096

# Define the header and some sample data
header = ["Rank", "Sequence", "Adjusted Sum", "Length", "Sum", "Image Cardinality", "Image", "Is Strictly Increasing",
          "Is RGF Sequence"]
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
            s: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.AdjustedSumFirstLengthSecondLexicographicThirdOrder.successor(
                s)
        record = [rank, s,
                  pu.nn0sl.AdjustedSumFirstLengthSecondLexicographicThirdOrder.get_adjusted_sum(s),
                  s.length, s.sum, s.image_cardinality, s.image, s.is_strictly_increasing,
                  s.is_restricted_growth_function_sequence]
        csvwriter.writerow(record)
