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


def process(i,j, ic, jc, k, sigma, picture):
  from skimage.draw import polygon
  # 遍历图像中的每个点
  p = Point(i, j, ic, jc, k, sigma)
  # 如果点的状态为1，则生成一个碎片
  if p.status() == 1:
    area = p.area()
    if area <= 0:
      area = 0.0001
    a = random.normalvariate(area**(1/2), p.sigma/2)

    # 计算碎片的四个顶点
    x1, y1 = i - a/2, j - a/2
    x2, y2 = i + a/2, j - a/2
    x3, y3 = i + a/2, j + a/2
    x4, y4 = i - a/2, j + a/2

    # 计算多边形的坐标
    rr, cc = polygon([y1, y2, y3, y4, y1], [x1, x2, x3, x4, x1])

    # 确保坐标在图像范围内
    rr = np.clip(rr, 0, picture.shape[0]-1)
    cc = np.clip(cc, 0, picture.shape[1]-1)

    # 计算新的灰度值
    gray_pic = picture[rr, cc]
    m = np.minimum(gray_pic - p.gray(), gray_pic + p.gray())
    n = np.maximum(gray_pic - p.gray(), gray_pic + p.gray())
    gray_value = np.random.randint(m, n, size=gray_pic.shape)

    # 将新的灰度值应用到碎片区域
    picture[rr, cc] = gray_value

def process_picture(dm, dn, ic, jc, k, sigma, picture):
  max_dim = np.argmax(picture.shape)
  # If the longer side is the height (dimension 0), iterate over i
  if max_dim == 0:
    for j in np.arange(0, picture.shape[0], dm):
      for i in np.arange(0, picture.shape[1], dn):
        process(i, j, ic, jc, k, sigma, picture)

  # If the longer side is the width (dimension 1), iterate over j
  else:
    for i in np.arange(0, picture.shape[1], dn):
      for j in np.arange(0, picture.shape[0], dm):
        process(i, j, ic, jc, k, sigma, picture)

  return picture
