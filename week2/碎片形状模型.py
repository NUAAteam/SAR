import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
#进来的一个x，一个y，一个theta
#x的值是i*dm，y的值是j*dn，即一个碎片中心


#2）第二步，一样的，暂时但是会最终得到一个ab

#3）第三步，随机取点
    #首先，确定任意一个碎片中心处构成的四边形在坐标上的范围（i*dm-a/2，i*dm+a/2），（j*dn-b/2，j*dn+b/2）

    #生成四个点


#DDA算法
def DDA(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    k = dy/dx
    x, y = x1, y1
    #网格线
    plt.grid()
    #x轴y轴数值取整
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    #绘点
    for i in range(0, int(abs(dx)+1)):
        #需要四舍五入
        plt.plot(int(round(x)), int(round(y)), 'b.', markersize = 1)
        x += 1
        y += float(k)
    plt.show()

def S(i,j,dm,dn,m,n,theta):
    r = (dm*(i-(m-1)/2))**2+ (dn*(j-(n-1)/2))**2
    s = (np.random.normal(loc=r,scale=theta))/(r**2)
    return s

def a_b(s,theta):
    a = np.random.normal(loc=math.sqrt(s),scale=0.5*theta)
    return a


#首先不会调用文件，按照预想的应该有m,n,dm,dn,i,j之类，还有前面的那些数组进来，具体看下面标黄线的即可
if __name__ == "__main__":
    S_array = [[0.0 for _ in range(n)] for _ in range(m)]
    a_array = [[0.0 for _ in range(n)] for _ in range(m)]
    b_array = [[0.0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if X_array[i][j] == 1:
                s = S(i,j,dm,dn,m,n,theta)
                a_array[i][j] = a_b(s,theta)
                b_array[i][j] = s/(a_b(s,theta))
                #生成四个点
                #point1
                x1 = i*dm-a_array[i][j]/2
                y1 = random.uniform(j*dn-b_array[i][j]/2,j*dn+b_array[i][j]/2)
                #point2
                x2 = random.uniform(i*dm-a_array[i][j]/2,i*dm+a_array[i][j]/2)
                y2 = j*dn-b_array[i][j]/2
                #point3
                x3 = i*dm+a_array[i][j]/2
                y3 = random.uniform(j*dn-b_array[i][j]/2,j*dn+b_array[i][j]/2)
                #point4
                x4 = random.uniform(i*dm-a_array[i][j]/2,i*dm+a_array[i][j]/2)
                y4 = j*dn+b_array[i][j]/2

                #DDA算法line1
                x,y = x1,y1
                xEnd, yEnd = x2,y2
                if xEnd < x:
                    x,y, xEnd, yEnd = xEnd, yEnd, x, y
                DDA(x, y, xEnd, yEnd)
                #DDA算法line2
                x,y = x2,y2
                xEnd, yEnd = x3,y3
                if xEnd < x:
                    x,y, xEnd, yEnd = xEnd, yEnd, x, y
                DDA(x, y, xEnd, yEnd)
                #DDA算法line3
                x,y = x3,y3
                xEnd, yEnd = x4,y4
                if xEnd < x:
                    x,y, xEnd, yEnd = xEnd, yEnd, x, y
                DDA(x, y, xEnd, yEnd)
                #DDA算法line4
                x,y = x4,y4
                xEnd, yEnd = x1,y1
                if xEnd < x:
                    x,y, xEnd, yEnd = xEnd, yEnd, x, y
                DDA(x, y, xEnd, yEnd)

