from random import random
from itertools import groupby
import matplotlib.pyplot as plt

# Your existing code

rands = (random() for _ in range(100000))


def group(numbers, split_in_number_of_parts=25):
    numbers = sorted(
        int((n * split_in_number_of_parts)) / split_in_number_of_parts for n in numbers
    )
    numbers = [
        (str(round(key + 1 / split_in_number_of_parts / 2 , 3)), len(list(group)))
        for key, group in groupby(numbers)
    ]
    return numbers


data = group(rands)

# Extract x and y values from the data
x = [item[0] for item in data]
y = [item[1] for item in data]

# Create a bar plot
plt.bar(x, y)

# Add labels and title
plt.xlabel("Value")
plt.ylabel("Count")
plt.title("Bar Plot")

# Display the plot
plt.show()
