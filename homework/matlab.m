
r0 = 300;
q0 = pi/3;
sigma0 = pi/6;
eta0 = q0-sigma0;
sigma_m0 = pi/4;
eta_m0 = q0 - sigma_m0;

y0 = [r0; q0; sigma0; eta0; sigma_m0; eta_m0];
yp0 = [0; 0; 0; 0; 0; 0];  % initial derivatives

tspan = [0 10];
[t, y] = ode15i(@dae, tspan, y0, yp0);

% Plot r curve
figure;
plot(t, y(:, 1));
title('r over time');
xlabel('Time');
ylabel('r');
grid on;

function res = dae(t, y, yp)
    V_m = 30;
    V_d = 50;
    sigma_m = pi/4;
    q_0 = pi/3;
    eta_m = q_0 - sigma_m;

    r = y(1);
    drdt = yp(1);
    q = y(2);
    dqdt = yp(2);
    sigma = y(3);
    eta = y(4);
    sigma_m = y(5);
    eta_m = y(6);

    res = zeros(6, 1);

    res(1) = drdt - V_m*cos(eta_m) + V_d*cos(eta);
    res(2) = dqdt - V_d*sin(eta) + V_m*sin(eta_m);
    res(3) = q - sigma - eta;
    res(4) = q - sigma_m - eta_m;
    res(5) = q - q_0;
    res(6) = 0;  % epsilon = 0
end

