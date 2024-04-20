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
    #TODO 验证公式正确性
    # 计算点的面积（正态分布N(dist, sigma))
    def area(self):
        return random.normalvariate(self.dist(), self.sigma)
    # 计算点的灰度值变动幅度
    def gray(self):
        v= int(200*self.sigma**2/(self.dist()+0.00001))
        if v>=127:
            v=127
        return v


def draw_many_splinter(dm, dn, ic, jc, k, sigma,picture):
    data=[]

    for i in np.arange(0, 100, dm):
        for j in np.arange(0, 100, dn):
            p = Point(i, j, ic, jc, k, sigma)
            if p.status() == 1:
                area=p.area()
                if area<=0:
                    area=0.0001
                a=random.normalvariate(area**(1/2), p.sigma/2)
                x1 = i-a/2
                y1 = random.uniform(j-a/2,j+a/2)
                x3 = i+a/2
                y3 = random.uniform(j-a/2,j+a/2)

                x2 = random.uniform(i-a/2,i+a/2)
                y2 = j-a/2
                x4 = random.uniform(i-a/2,i+a/2)
                y4 = j+a/2

                gray_pic = picture[int(i), int(j)]
                m = gray_pic - p.gray()
                n = gray_pic + p.gray()
                gray_value = random.randint(m, n)
                gray_color = 'rgb({0}, {0}, {0})'.format(gray_value)
                data.append(go.Scatter(x=[x1, x2, x3, x4, x1, None],
                                       y=[y1, y2, y3, y4, y1, None],
                                       mode='lines',
                                       line=dict(color=gray_color, width=1),
                                       fill='toself',
                                       fillcolor=gray_color))
    fig = go.Figure(data=data)

    return fig
