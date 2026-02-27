import sympy
import pprint

x = sympy.symbols('x')

print("Series for sin(x):")
pprint.pprint((sympy.sin(x)**5).series(x, 0, 10))
