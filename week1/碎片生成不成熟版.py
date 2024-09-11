import numpy as np
import matplotlib.pyplot as plt
import math
import random

# 输入l1和l2的值
k = 1500
l1 = int(input("请输入一个打击等级："))  # l1为打击等级
l2 = int(input("请输入一个目标材质等级："))  # l2为目标材质等级

# 输入n的值
n = int(input("请输入n的值："))
# 计算m的值
m = l1 / l2

# 输入R(i,j)坐标
R = np.zeros((n, n))  # 假设n为矩阵的大小
for i in range(n):
    for j in range(n):
        R = input("请输入R({},{})的值：".format(i, j))

# 生成随机数矩阵rand
rand = np.random.randint(0, 2)

# 计算X(i, j)的值
X = 1 - np.int_(rand + 1 - np.exp((-R**2) / (k * m)))

# 绘制像素点图像
plt.imshow(X, cmap='gray')  # 使用灰度图显示
plt.show()
