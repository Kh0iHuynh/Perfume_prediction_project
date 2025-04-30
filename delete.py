import csv

file_path = "perfume_data.csv"  # Make sure this path is correct
with open(file_path, 'r') as file:
    reader = csv.reader(file, delimiter='\t')  # Try using tab delimiter
    for i, row in enumerate(reader):
        if i < 10:  # Print the first 10 rows to inspect
            print(row)

