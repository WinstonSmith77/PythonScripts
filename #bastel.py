from sympy import symbols, Eq, solve, expand, factor, collect, simplify

# Define the variable
x = symbols('x')

# Define the coefficients

b = symbols('b')
c = symbols('c')


# Define the equation
equation = Eq(x**5 + b * x + c, 0)

# Solve the equation
roots = solve(equation, x)
print("The roots are:", roots)