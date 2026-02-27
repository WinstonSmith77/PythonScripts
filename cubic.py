import sympy
from pprint import pprint

a, b, c, d, x1, x2, y1, y2, k1, k2 = sympy.symbols('a b c d x1 x2 y1 y2 k1 k2')
eq1 = a*x1**3 + b*x1**2 + c*x1 + d - y1
eq2 = a*x2**3 + b*x2**2 + c*x2 + d - y2
eq3 = 3*a*x1**2 + 2*b*x1 + c - k1
eq4 = 3*a*x2**2 + 2*b*x2 + c - k2
sol = sympy.solve([eq1, eq2, eq3, eq4], [a, b, c, d])


for k,v in sol.items():
    print('var ', k,'=',sympy.ccode(v), ";")
