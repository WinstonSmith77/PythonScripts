import sympy

g, k = sympy.symbols("g k")
s = sympy.solve((g+k)/g - g / k, g)

print(s)