import csv

path = r"C:\Users\henning\Downloads\61111-0002_de.csv"
data = []
with open(path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    
    # Skip the header rows
    for _ in range(5):
        next(reader)
    
    # Read data rows
    for row in reader:
      
        if len(row) >= 2 and row[1] and row[1] != '...':  # Check if month column exists and is not empty or '...'
            # If first column is empty, use content from previous non-empty first column
            if not row[0] and data:
                # Find the last non-empty first column value
                for prev_row in reversed(data):
                    if prev_row[0]:
                        row[0] = prev_row[0]
                        break
            # Handle the value in row[6]: if "-" use 0, else parse as float with ',' as decimal separator
            value = 0 if (row[6] == "-" or row[6] == "...") else float(row[6].replace(',', '.'))
            row = [row[0], row[1], value]
            data.append(row)

# Print first few rows
for i, row in enumerate(data):
    print(row)