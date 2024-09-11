from random import random
from itertools import groupby
import matplotlib.pyplot as plt

# Your existing code

rands = (random() for _ in range(10000))

def group(numbers, factor=20):
    numbers = sorted(int((n * factor)) / factor for n in numbers)
    numbers = [(key,len(list(group))) for key, group in groupby(numbers)]
    return numbers

data = group(rands)

# Extract x and y values from the data
x = [str(item[0]) for item in data]
y = [item[1] for item in data]

# Create a bar plot
plt.bar(x, y)

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Count')
plt.title('Bar Plot')

# Display the plot
plt.show()