from scipy.integrate import odeint  # 导入 scipy.integrate 模块
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 导数函数, 求 W=[x,y,z] 点的导数 dW/dt
def lorenz(W, t, p, r, b):
    x, y, z = W  # W=[x,y,z]
    dx_dt = p * (y - x)  # dx/dt = p*(y-x), p: sigma
    dy_dt = x * (r - z) - y  # dy/dt = x*(r-z)-y, r:rho
    dz_dt = x * y - b * z  # dz/dt = x*y - b*z, b;beta
    return np.array([dx_dt, dy_dt, dz_dt])


t = np.arange(0, 30, 0.01)  # 创建时间点 (start,stop,step)
paras = (10.0, 28.0, 3.0)  # 设置 Lorenz 方程中的参数 (p,r,b)

# 调用ode对lorenz进行求解, 用两个不同的初始值 W1、W2 分别求解
W1 = (0.0, 1.00, 0.0)  # 定义初值为 W1
track1 = odeint(lorenz, W1, t, args=(10.0, 28.0, 3.0))  # args 设置导数函数的参数
W2 = (0.0, 1.01, 0.0)  # 定义初值为 W2
track2 = odeint(lorenz, W2, t, args=paras)  # 通过 paras 传递导数函数的参数

# 绘图
fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)
ax.plot(track1[:, 0], track1[:, 1], track1[:, 2], color='magenta')  # 绘制轨迹 1
ax.plot(track2[:, 0], track2[:, 1], track2[:, 2], color='deepskyblue')  # 绘制轨迹 2
ax.set_title("Lorenz attractor by scipy.integrate.odeint")
plt.show()
