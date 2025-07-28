import csv
import punctilious as pu

# Define the CSV file name
filename = "natural_number_0_pair_list.csv"
list_size = 2048

# Define the header and some sample data
header = ["Rank", "Pair", "Length", "Image Cardinality", "Image", "Is Strictly Increasing", "Is RGF Sequence"]
data = []

# Writing to the CSV file with pipe separator
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="|")
    csvwriter.writerow(header)
    for rank in range(list_size):
        if rank == 0:
            s: pu.nn0pl.NaturalNumber0Pair = pu.nn0pl.NaturalNumber0Pair.least_element
        else:
            s: pu.nn0pl.NaturalNumber0Pair = s.successor()
        record = [rank, s, s.length, s.image_cardinality, s.image, s.is_strictly_increasing,
                  s.is_restricted_growth_function_sequence]
        csvwriter.writerow(record)
