import numpy as np
import matplotlib.pyplot as plt

def cubic_bezier(P0, P1, P2, P3, t):
    return (1-t)**3 * P0 + 3*(1-t)**2*t * P1 + 3*(1-t)*t**2 * P2 + t**3 * P3

def bezier_derivative(P0, P1, P2, P3, t):
    return 3*(1-t)**2 * (P1-P0) + 6*(1-t)*t * (P2-P1) + 3*t**2 * (P3-P2)

def solve_bezier_for_x(P0, P1, P2, P3, x, epsilon=1e-6, max_iterations=100):
    t = 0.5  # Initial guess
    for _ in range(max_iterations):
        current_x = cubic_bezier(P0, P1, P2, P3, t)[0]
        if abs(current_x - x) < epsilon:
            return t
        derivative = bezier_derivative(P0, P1, P2, P3, t)[0]
        if derivative == 0:
            break
        t = t - (current_x - x) / derivative
    return t  # Return best approximation if max iterations reached

# Define control points
P0 = np.array([0, 0])
P1 = np.array([1, -3])
P2 = np.array([3, 13])
P3 = np.array([4, 0])

# Generate points on the curve
t = np.linspace(0, 1, 100)
curve = np.array([cubic_bezier(P0, P1, P2, P3, t_i) for t_i in t])


x_target = 2.5
t_target = solve_bezier_for_x(P0, P1, P2, P3, x_target)

PX = cubic_bezier(P0, P1, P2, P3, t_target)


# Print results

# Plot
plt.figure(figsize=(10, 6))
plt.plot(curve[:, 0], curve[:, 1], 'b-', label='Bézier Curve')
plt.plot([P0[0], P1[0], P2[0], P3[0]], [P0[1], P1[1], P2[1], P3[1]], 'ro-', label='Control Points')
plt.plot([PX[0]], [PX[1]], 'go-', label=f'Point on Curve with {x_target:.2f} x-coordinate')
plt.legend()
plt.title('Cubic Bézier Curve')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axis('equal')
plt.show()
