from sympy import Function, dsolve, Derivative, symbols, solve, Eq
from sympy.abc import t
import numpy as np
from sympy import lambdify
import matplotlib.pyplot as plt

T = Function("T")
T0 = symbols('T0')
# Solve the ODE
ode = Derivative(T(t), t) - (T0 - T(t))
print(ode)
result = dsolve(ode, T(t))
print(result)

# Choose a value for t0
t0_val = 20

# Get the general solution and substitute t0
sol = result.rhs.subs(T0, t0_val)

# Find C1 so that y(0) = 25
C1 = symbols('C1')
# The general solution has C1 in it, so solve for C1
sol_with_C1 = sol.subs('C1', C1)
eq = Eq(sol_with_C1.subs(t, 0), 22)
C1_val = solve(eq, C1)[0]
# Substitute C1 back into the solution
sol_final = sol.subs('C1', C1_val)

# Create a numerical function
f = lambdify(t, sol_final, modules=['numpy'])

# Plot
x_vals = np.linspace(-2, 10, 400)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals, label=f't0={t0_val}, T(0)=25')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Solution of dT/dt = t0 - T with T(0)=25')
plt.legend()
plt.grid(True)
plt.show()
