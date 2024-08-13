import sympy as sp
from pprint import pprint


# Define the symbol and the expression for the sum
n = sp.symbols('n')
expr = 1/(4**n)

# Calculate the infinite sum
result = sp.summation(expr, (n, 0, sp.oo))


# Print the result
pprint(result)