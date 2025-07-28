import csv
import punctilious as pu

# Define the CSV file name
filename = "dyck_word_list.csv"
list_size = 2048

# Define the header and some sample data
header = ["Rank", "Dyck Word", "Characters Number"]
data = []

# Writing to the CSV file with pipe separator
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="|")
    csvwriter.writerow(header)
    for rank in range(list_size):
        if rank == 0:
            w: pu.dwl.DyckWord = pu.dwl.DyckWord.least_element
        else:
            w: pu.dwl.DyckWord = w.successor()
        record = [rank, w, w.characters_number]
        csvwriter.writerow(record)
