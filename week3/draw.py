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
#假设碎片的长宽比为1：1
#碎片中心点为i，j
#碎片面积为area
#在碎片的每个边上随机选取 1 个点，得到四个随机点
#采用计算机图形学中的数值微分直线生成法连接四个点，得到一个碎片
#生成所有碎片

# 融合picture与碎片
# 方法： 取图像中i,j点的灰度值，然后加减碎片的灰度变动幅度
    for i in np.arange(0, 100, dm):
        for j in np.arange(0, 100, dn):
            p = Point(i, j, ic, jc, k, sigma)
            # 取图像中i,j点的灰度值
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

#碎片内部灰度值为均匀分布U(m,n)的结果，碎片是实心的
#m=127灰度-p.gray()
#n=127灰度+p.gray()
                # Calculate the gray color for each splinter
                #重点就是要把这个127换成实际的从图像中读取的灰度值
                #TODO 从图像中读取灰度值
                # 可能的办法：1. 读取图像，2. 传递图像数据给draw.py 3. 从图像数据中获取灰度值 4. 用灰度值替换127
                # 取图像中i,j点的灰度值
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
