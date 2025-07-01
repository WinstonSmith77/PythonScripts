from sympy import Function, dsolve, Derivative, symbols, solve, Eq
from sympy.abc import x
import numpy as np
from sympy import lambdify
import matplotlib.pyplot as plt

y = Function("y")
t0 = symbols('t0')
# Solve the ODE
result = dsolve(Derivative(y(x), x) - (t0 - y(x)), y(x))
print(result)

# Choose a value for t0
t0_val = 20

# Get the general solution and substitute t0
sol = result.rhs.subs(t0, t0_val)

# Find C1 so that y(0) = 25
C1 = symbols('C1')
# The general solution has C1 in it, so solve for C1
sol_with_C1 = sol.subs('C1', C1)
eq = Eq(sol_with_C1.subs(x, 0), 22)
C1_val = solve(eq, C1)[0]
# Substitute C1 back into the solution
sol_final = sol.subs('C1', C1_val)

# Create a numerical function
f = lambdify(x, sol_final, modules=['numpy'])

# Plot
x_vals = np.linspace(-2, 10, 400)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals, label=f't0={t0_val}, y(0)=25')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Solution of dy/dx = t0 - y with y(0)=25')
plt.legend()
plt.grid(True)
plt.show()
