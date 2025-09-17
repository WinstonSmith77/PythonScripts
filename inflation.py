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
            row = [row[0], row[1], row[6]]  # Replace comma with dot for decimal conversion
            data.append(row)

# Print first few rows
for i, row in enumerate(data):
    print(row)