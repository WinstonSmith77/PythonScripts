import numpy as np
import matplotlib.pyplot as plt

def simulate_grenade_trajectory(v0, angle, dt=0.01, drag_coefficient=0.47, cross_sectional_area=0.01, mass=5.0):
    """
    Simulate the trajectory of an artillery grenade with air resistance.
    
    Parameters:
    v0: initial velocity (m/s)
    angle: launch angle (degrees)
    dt: time step (seconds)
    drag_coefficient: dimensionless drag coefficient (default 0.47 for sphere)
    cross_sectional_area: cross-sectional area (m^2)
    mass: mass of grenade (kg)
    """
    g = 9.81  # acceleration due to gravity (m/s^2)
    rho = 1.225  # air density at sea level (kg/m^3)
    angle_rad = np.radians(angle)
    
    # Initial velocity components
    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)
    
    # Lists to store trajectory data
    x_vals = [0]
    y_vals = [0]
    x, y = 0, 0
    
    # Simulate until grenade hits the ground
    while y >= 0:
        # Calculate velocity magnitude
        v = np.sqrt(vx**2 + vy**2)
        
        # Calculate drag force magnitude
        F_drag = 0.5 * rho * drag_coefficient * cross_sectional_area * v**2
        
        # Calculate drag acceleration components
        ax = -(F_drag / mass) * (vx / v) if v > 0 else 0
        ay = -g - (F_drag / mass) * (vy / v) if v > 0 else -g
        
        # Update velocities
        vx += ax * dt
        vy += ay * dt
        
        # Update positions
        x += vx * dt
        y += vy * dt
        
        if y < 0:
            break
            
        x_vals.append(x)
        y_vals.append(y)
    
    return x_vals, y_vals

# Example usage
initial_velocity = 1500  # m/s
angles = range(30, 60, 3)  # 10 to 45 degrees in 5-degree steps

# Plot the trajectories
plt.figure(figsize=(12, 8))
for angle in angles:
    x, y = simulate_grenade_trajectory(initial_velocity, angle)
    plt.plot(x, y, linewidth=2, label=f'{angle}°')

plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title(f'Artillery Grenade Trajectories with Air Resistance (v0={initial_velocity} m/s)')
plt.grid(True)
plt.legend()
plt.show()
