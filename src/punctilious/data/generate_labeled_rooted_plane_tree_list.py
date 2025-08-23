import csv
import punctilious as pu

# Define the CSV file name
filename = "labeled_rooted_plane_tree_list.csv"
list_size = 4096

# Define the header and some sample data
header = ["Rank", "LRPT", "RPT", "NN0S", "Im(NN0S)", "Main Element", "Arity", "Is Canonical",
          "Is Strictly Increasing", "RPT Rank", "Sequence Rank", "Sequence Max Value"]
data = []

# Writing to the CSV file with pipe separator
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="|")
    csvwriter.writerow(header)
    for rank in range(list_size):
        if rank == 0:
            phi: pu.lrptl.LabeledRootedPlaneTree = pu.lrptl.LabeledRootedPlaneTree.least_element
        else:
            phi: pu.lrptl.LabeledRootedPlaneTree = phi.successor
        record = [rank,
                  phi,
                  phi.rooted_plane_tree,
                  phi.natural_number_sequence,
                  phi.natural_number_sequence.image,
                  phi.root_label,
                  phi.degree,
                  phi.is_canonical,
                  phi.is_strictly_increasing,
                  phi.rooted_plane_tree.rank,
                  phi.natural_number_sequence.rank,
                  phi.sequence_max_value,
                  ]
        csvwriter.writerow(record)
