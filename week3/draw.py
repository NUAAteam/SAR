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
    # 计算点的面积（正态分布N(dist, sigma))
    def area(self):
        return random.normalvariate(self.dist(), self.sigma)

# 初始值
# 间隔
dn=1
dm=1

# 中心点在图像中的位置(百分比)
ic=50
jc=50

# 打击参数
k=500
sigma=1

def draw_many_splinter(dm, dn, ic, jc, k, sigma):
    x = []
    y = []
#假设碎片的长宽比为1：1
#碎片中心点为i，j
#碎片面积为area
#在碎片的每个边上随机选取 1 个点，得到四个随机点
#采用计算机图形学中的数值微分直线生成法连接四个点，得到一个碎片
#生成所有碎片

    for i in np.arange(0, 100, dm):
        for j in np.arange(0, 100, dn):
            p = Point(i, j, ic, jc, k, sigma)
            if p.status() == 1:
                a=random.normalvariate(p.area()**(1/2), p.sigma/2)
                x1 = i-a/2
                y1 = random.uniform(j-a/2,j+a/2)
                x3 = i+a/2
                y3 = random.uniform(j-a/2,j+a/2)

                x2 = random.uniform(i-a/2,i+a/2)
                y2 = j-a/2
                x4 = random.uniform(i-a/2,i+a/2)
                y4 = j+a/2
                x.extend([x1, x2, x3, x4, x1, None])
                y.extend([y1, y2, y3, y4, y1, None])
    fig = go.Figure(data=go.Scattergl(x=x, y=y, mode='lines',
                                      line=dict(color='blue', width=1)))
#碎片内部灰度值为均匀分布U(m,n)的结果，碎片是实心的
#v = 150*sigma/dist()
#m=原灰度-v
#n=原灰度+v


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
