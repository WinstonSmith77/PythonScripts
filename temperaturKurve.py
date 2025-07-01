from sympy import Function, dsolve, Derivative
from sympy.abc import x, c
import numpy as np
from sympy import lambdify
import matplotlib.pyplot as plt

y = Function("y")
# Solve the ODE


result = dsolve(Derivative(y(x), x) - (c - y(x)), y(x))
print(result)

# Choose a value for c
c_val = 20

# Get the general solution and substitute c
sol = result.rhs.subs(c, c_val)

# Substitute the integration constant with a value, e.g., C1=0
sol = sol.subs('C1', 1)

# Create a numerical function
f = lambdify(x, sol, modules=['numpy'])

# Plot
x_vals = np.linspace(0, 10, 400)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals, label=f'c={c_val}')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Solution of dy/dx = c - y')
plt.legend()
plt.grid(True)
plt.show()
