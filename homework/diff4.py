from pyomo.environ import *
from pyomo.dae import *
import numpy as np

m = ConcreteModel()

# 定义时间域
m.t = ContinuousSet(bounds=(0.0, 1.0))

# 定义变量
m.r = Var(m.t, domain=Reals)
m.eta = Var(m.t, domain=Reals)
m.sigma = Var(m.t, domain=Reals)
m.sigma_m = Var(m.t, domain=Reals)

# 定义微分变量
m.dr = DerivativeVar(m.r, wrt=m.t)
m.dq = DerivativeVar(m.sigma, wrt=m.t)

# 已知量
q0=np.pi/3
sigma0=np.pi/6
sigma_m0=np.pi/4
V_d = 50  # 请在这里填入你的值
V_m = 30  # 请在这里填入你的值
eta_m = q0-sigma_m0  # Define eta_m


# 定义DAE方程
def _dae1(m, t):
    return m.dr[t] == V_m*cos(eta_m) - V_d*cos(m.eta[t])

m.dae1 = Constraint(m.t, rule=_dae1)

def _dae2(m, t):
    return m.r[t]*m.dq[t] == V_d*sin(m.eta[t]) - V_m*sin(eta_m)

m.dae2 = Constraint(m.t, rule=_dae2)

def _dae3(m, t):
    return q0 == m.sigma[t] + m.eta[t]

m.dae3 = Constraint(m.t, rule=_dae3)

def _dae4(m, t):
    return q0 == m.sigma_m[t] + eta_m

m.dae4 = Constraint(m.t, rule=_dae4)

def _dae5(m, t):
    return 0 == m.dq[t]

m.dae5 = Constraint(m.t, rule=_dae5)

# 选择一个求解器
solver = SolverFactory('ipopt')

# 求解模型
results = solver.solve(m, tee=True)
