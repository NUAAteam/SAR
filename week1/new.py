import math
import random
import matplotlib.pyplot as plt
import numpy as np
import asyncio

import nest_asyncio
nest_asyncio.apply()



class Point:
    def __init__(self, i, j, ic, jc, k, sigma):
        # i, j: 点坐标
        self.i = i
        self.j = j
        # ic, jc: 中心点坐标
        self.ic = ic
        self.jc = jc
        # k, sigma: 打击参数
        self.k = k
        self.sigma = sigma

# 计算点到中心点的距离
    def dist(self):
        return ((self.i-self.ic)**2 + (self.j-self.jc)**2)**0.5

# 计算点的概率
    def pab(self):
        return math.exp(-self.dist()**2/(self.k*self.sigma))

# 计算点成为碎片点的状态，1为是，0为否
    def status(self):
        return 1-int(random.random()+1-self.pab())

# 图像大小
width=10
height=10

# 间隔
dn=1
dm=1

# 中心点在图像中的位置(百分比)
ic=50
jc=50

# 打击参数
k=500
sigma=1

async def draw_point(i, j, ic, jc, k, sigma):
    p = Point(i, j, ic, jc, k, sigma)
    if p.status() == 1:
        plt.scatter(j, i, s= 1, color='b')  # Note that j is the x-coordinate and i is the y-coordinate

def draw_many_points(width,height,dm, dn, ic, jc, k, sigma, draw_point):
  plt.figure(figsize=(width, height))
  # Create and draw the points
  loop = asyncio.get_event_loop()
  tasks = []
  for i in np.arange(0, 100, dm):
    for j in np.arange(0, 100, dn):
      task = loop.create_task(draw_point(i, j, ic, jc, k, sigma))
      tasks.append(task)
  loop.run_until_complete(asyncio.gather(*tasks))
  # Show the picture
  plt.show()

# Show the picture
draw_many_points(width,height,dm, dn, ic, jc, k, sigma, draw_point)