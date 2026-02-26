import sympy

# Define symbols
a, b, c, d, e, f = sympy.symbols('a b c d e f')
x1, x2 = sympy.symbols('x1 x2')
y1, y2 = sympy.symbols('y1 y2')       # Position f(x)
k1, k2 = sympy.symbols('k1 k2')       # Velocity f'(x)
m1, m2 = sympy.symbols('m1 m2')       # Acceleration f''(x)

# 1. Position equations: f(x)
eq1 = a*x1**5 + b*x1**4 + c*x1**3 + d*x1**2 + e*x1 + f - y1
eq2 = a*x2**5 + b*x2**4 + c*x2**3 + d*x2**2 + e*x2 + f - y2

# 2. Velocity equations: f'(x) = 5ax^4 + 4bx^3 + 3cx^2 + 2dx + e
eq3 = 5*a*x1**4 + 4*b*x1**3 + 3*c*x1**2 + 2*d*x1 + e - k1
eq4 = 5*a*x2**4 + 4*b*x2**3 + 3*c*x2**2 + 2*d*x2 + e - k2

# 3. Acceleration equations: f''(x) = 20ax^3 + 12bx^2 + 6cx + 2d
eq5 = 20*a*x1**3 + 12*b*x1**2 + 6*c*x1 + 2*d - m1
eq6 = 20*a*x2**3 + 12*b*x2**2 + 6*c*x2 + 2*d - m2

print("Solving system...")
sol = sympy.solve([eq1, eq2, eq3, eq4, eq5, eq6], [a, b, c, d, e, f])

print("Solutions found:")
for k, v in sol.items():
    print(f"\n{k} =")
    print(sympy.simplify(v))