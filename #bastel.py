import sympy as sp
import pprint

# Define symbolic variables
x = sp.Symbol('x')
left = x**4
right = (x- 1)**4
solutions = sp.solve(left - right, x)

# # Define an expression
# expr = x**2 + 2*x*y + y**2

# # Simplify the expression
# simplified_expr = sp.simplify(expr)

# # Differentiate the expression with respect to x
# diff_expr = sp.diff(expr, x)

# # Integrate the expression with respect to y
# int_expr = sp.integrate(expr, y)

# # Solve the equation expr = 0
# solutions = sp.solve(expr, x)

# Print the results

pprint.pprint(solutions)