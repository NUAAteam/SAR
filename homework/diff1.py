from scipy.integrate import solve_ivp
import numpy as np

def system(t, y, V_m, V_d, eta_m):
  r, q, sigma, sigma_m, eta = y

  drdt = V_m * np.cos(eta_m) - V_d * np.cos(eta)
  dqdt = (V_d * np.sin(eta) - V_m * np.sin(eta_m)) / r
  dsigma_dt = dqdt - eta
  dsigma_m_dt = dqdt - eta_m
  detadt = 0

  return [drdt, dqdt, dsigma_dt, dsigma_m_dt, detadt]

r0=300
q0=np.pi/3
sigma0=np.pi/6
sigma_m0=np.pi/4
eta0=q0-sigma0

# Define the initial conditions
y0 = [r0, q0, sigma0, sigma_m0, eta0]  # Initial conditions

t_start=0
t_end=100

# Define the time span
t_span = [t_start, t_end]  # Time span

# Define the known parameters
V_m = 30  # Define V_m
V_d = 50  # Define V_d
eta_m = q0-sigma_m0  # Define eta_m

# Solve the system of differential equations
sol = solve_ivp(system, t_span, y0, args=(V_m, V_d, eta_m), method='BDF')

# The solution is then
r = sol.y[0]
q = sol.y[1]
sigma = sol.y[2]
sigma_m = sol.y[3]
eta = sol.y[4]
#print(r, q, sigma, sigma_m, eta)

import matplotlib.pyplot as plt

# Calculate the new r and sigma_m values
r_m = r0 + V_m * sol.t*np.cos(eta_m)

# Convert the new polar coordinates to Cartesian coordinates
x_m = r_m * np.cos(q0)
y_m = r_m * np.sin(q0)

# Calculate the absolute r and q values

# Convert the absolute polar coordinates to Cartesian coordinates
x_d = x_m-r*np.cos(q)
y_d = y_m-r*np.sin(q)

# Plot the trajectories
plt.figure(figsize=(6, 6))
plt.plot(x_m, y_m, label='New trajectory')
plt.plot(x_d, y_d, label='Absolute trajectory')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Trajectories in Cartesian coordinates')
plt.grid(True)
plt.axis('equal')  # Ensure the aspect ratio is correct
plt.legend()
plt.show()
