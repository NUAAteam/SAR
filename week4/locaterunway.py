import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objs as go
import cv2

# 加载图像
img_path = 'C:/Users/Lenovo/Desktop/SAR/week4/runway.jpg'
img = Image.open(img_path)
img_array = np.array(img)

# 转换为灰度图像
gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

# 创建Plotly图像
fig = go.Figure(data=go.Heatmap(z=gray_img, colorscale='gray', showscale=False))

# 获取用户输入的坐标
x = st.number_input('Enter x coordinate:', min_value=0, max_value=img.width-1, value=0, step=1)
y = st.number_input('Enter y coordinate:', min_value=0, max_value=img.height-1, value=0, step=1)

x, y = int(x), int(y)
# 获取种子点的灰度值
seed_value = gray_img[y, x]
st.write(f'The gray level of the seed point is: {seed_value}')

# 获取用户输入的增长准则
threshold = st.number_input('Enter growth criterion:', min_value=0, max_value=255, value=20, step=1)

from collections import deque

def region_growing(img, seed, threshold):
  # 创建一个和输入图像同样大小的布尔数组，用于标记访问过的像素
  visited = np.zeros_like(img, dtype=np.bool_)
  dx = [-1, 0, 1, 0]
  dy = [0, 1, 0, -1]
  queue = deque([seed])
  seed_value = int(img[seed])

  while queue:
    x, y = queue.popleft()
    if not visited[y, x] and abs(int(img[y, x]) - seed_value) <= threshold:
      visited[y, x] = True
      img[y, x] = 0
      for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < img.shape[1] and 0 <= ny < img.shape[0]:
          queue.append((nx, ny))
  return img

# 在主程序中使用区域增长算法
gray_img = region_growing(gray_img, (x, y), threshold)

# 更新Plotly图像
fig = go.Figure(data=go.Heatmap(z=gray_img, colorscale='gray', showscale=False))

# 在图像上添加十字线
fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=img.height, line=dict(color="Red", width=2))
fig.add_shape(type="line", x0=0, y0=y, x1=img.width, y1=y, line=dict(color="Red", width=2))

fig.update_layout(width=img.width, height=img.height, autosize=False)

# 显示图像
st.plotly_chart(fig)