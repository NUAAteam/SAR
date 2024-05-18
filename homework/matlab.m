%dr/dt=V_m*cos(eta_m)-V_d*cos(eta)
%r*dq/dt=V_d*sin(eta)-V_m*sin(eta_m)
%q=sigma+eta
%q=sigma_m+eta_m
%epsilon=0

% Define the initial conditions
r0 = 300;  % Define r0
q0 = pi/2;  % Define q0
eta0 = ...;  % Define eta0
sigma0 = q0-eta0;  % Define sigma0
sigma_m0 = ...;  % Define sigma_m0
% Define the initial conditions and the time span
y0 = [r0; q0; sigma0; sigma_m0; eta0];  % Initial conditions
tspan = [t_start t_end];  % Time span

% Define the known parameters
V_m = 20;  % Define V_m
V_d = 20;  % Define V_d
eta_m = pi/3;  % Define eta_m
eta = 0;  % Define eta

% Solve the system of differential equations
[t, y] = ode45(@(t, y) system(t, y, V_m, V_d, eta_m, eta), tspan, y0);
function dydt = system(t, y, V_m, V_d, eta_m, eta)
  % Define the variables
  r = y(1);
  q = y(2);
  sigma = y(3);
  sigma_m = y(4);
  eta = y(5);

  % Define the system of differential equations
  dydt = zeros(5, 1);
  dydt(1) = V_m*cos(eta_m) - V_d*cos(eta);  % dr/dt
  dydt(2) = (V_d*sin(eta) - V_m*sin(eta_m))/r;  % dq/dt
  dydt(3) = q - eta;  % sigma
  dydt(4) = q - eta_m;  % sigma_m
  %追踪法
  dydt(5) = 0;  % eta
end