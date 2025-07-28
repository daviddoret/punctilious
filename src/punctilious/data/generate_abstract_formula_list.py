import csv
import punctilious as pu

# Define the CSV file name
filename = "abstract_formula_list.csv"
list_size = 2048

# Define the header and some sample data
header = ["Rank", "Abstract Formula", "Main Element", "Arity", "Is Canonical",
          "Is Strictly Increasing", "RPT Rank", "Sequence Rank", "Sequence Max Value"]
data = []

# Writing to the CSV file with pipe separator
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="|")
    csvwriter.writerow(header)
    for rank in range(list_size):
        if rank == 0:
            phi: pu.afl.AbstractFormula = pu.afl.AbstractFormula.least_element
        else:
            phi: pu.afl.AbstractFormula = phi.successor()
        record = [rank, phi,
                  phi.main_element,
                  phi.arity,
                  phi.is_canonical,
                  phi.is_strictly_increasing,
                  phi.rooted_plane_tree.rank(),
                  phi.natural_number_sequence.rank(),
                  phi.sequence_max_value,
                  ]
        csvwriter.writerow(record)
