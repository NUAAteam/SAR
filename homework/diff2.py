from scipy.integrate import solve_ivp
import numpy as np

def system(t, y, V_m, V_d, eta_m, q0):
  r, eta = y

  drdt = V_m * np.cos(eta_m) - V_d * np.cos(eta)
  detadt = (V_d * np.sin(eta) - V_m * np.sin(eta_m)) / r

  return [drdt, detadt]


q0=np.pi/3
sigma0=np.pi/6
sigma_m0=np.pi/4
r0=300
eta0=q0-sigma0

# Define the initial conditions
y0 = [r0, eta0]  # Initial conditions

t_start=0
t_end=100

# Define the time span
t_span = [t_start, t_end]  # Time span

# Define the known parameters
V_m = 30  # Define V_m
V_d = 50  # Define V_d
eta_m = q0-sigma_m0  # Define eta_m
q0 = np.pi/3  # Define q0

# Solve the system of differential equations
sol = solve_ivp(system, t_span, y0, args=(V_m, V_d, eta_m, q0), method='BDF')

# The solution is then
r = sol.y[0]
eta = sol.y[1]

import matplotlib.pyplot as plt

# Plot r as a function of time
plt.figure(figsize=(10, 5))
plt.plot(sol.t, r)
plt.xlabel('Time')
plt.ylabel('r')
plt.title('r as a function of time')
plt.grid(True)
plt.show()