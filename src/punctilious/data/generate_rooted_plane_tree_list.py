import csv
import punctilious as pu

# Define the CSV file name
filename = "rooted_plane_tree_list.csv"
list_size = 2048

# Define the header and some sample data
header = ["Rank", "RPT", "Degree", "Is Strictly Increasing", "Size", "Dyck Word", "Is Leaf"]
data = []

# Writing to the CSV file with pipe separator
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="|")
    csvwriter.writerow(header)
    for rank in range(list_size):
        t: pu.rptl.RootedPlaneTree
        if rank == 0:
            t: pu.rptl.RootedPlaneTree = pu.rptl.RootedPlaneTree.least_element
        else:
            t: pu.rptl.RootedPlaneTree = t.successor()
        record = [rank, t, t.degree, t.is_strictly_increasing, t.size, t.dyck_word, t.is_leaf]
        csvwriter.writerow(record)
