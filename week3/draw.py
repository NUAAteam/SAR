import math
import random
import plotly.graph_objects as go
import numpy as np

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

# 间隔
dn=1
dm=1

# 中心点在图像中的位置(百分比)
ic=50
jc=50

# 打击参数
k=500
sigma=1

def draw_many_points(dm, dn, ic, jc, k, sigma):
    x = []
    y = []
    for i in np.arange(0, 100, dm):
        for j in np.arange(0, 100, dn):
            p = Point(i, j, ic, jc, k, sigma)
            if p.status() == 1:
                x.append(j)  # Note that j is the x-coordinate
                y.append(i)  # Note that i is the y-coordinate
    fig = go.Figure(data=go.Scattergl(x=x, y=y, mode='markers',
                                      marker=dict(color='blue', size=2)))
    #fig.show()
    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
        ),
    )
    return fig

