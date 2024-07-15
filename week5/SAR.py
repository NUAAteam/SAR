import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objs as go
import cv2
from collections import deque
import os
from cffi import FFI

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

# 加载图像
def low_pass_filter(image, cutoff):
    # Perform the Fourier transform
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    # Create a mask
    rows, cols = image.shape
    crow, ccol = int(rows/2), int(cols/2)
    mask = np.zeros((rows, cols), np.uint8)
    mask[crow-cutoff:crow+cutoff, ccol-cutoff:ccol+cutoff] = 1

    # Apply the mask and inverse Fourier transform
    fshift_masked = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_masked)
    img_back = np.fft.ifft2(f_ishift)

    return img_back
def sar():
  # 用户上传图像或使用默认图像
  uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
  if uploaded_file is not None:
      img = Image.open(uploaded_file)
  else:
    #注意这里也要修改vscode的工作路径，如果报错的话
      img_path =  os.path.abspath('./assets/runway.jpg')
      img = Image.open(img_path)
  img_array = np.array(img)

  # 转换为灰度图像
  gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

  # 创建Plotly图像
  fig = go.Figure(data=go.Heatmap(z=gray_img, colorscale='gray', showscale=False))

  # 获取用户输入的坐标
  if uploaded_file is None:
    x = st.number_input('Enter x coordinate:', min_value=0, max_value=img.width-1, value=555, step=1)
    y = st.number_input('Enter y coordinate:', min_value=0, max_value=img.height-1, value=632, step=1)
  else:
    x = st.number_input('Enter x coordinate:', min_value=0, max_value=img.width-1, value=int(img.width/2), step=1)
    y = st.number_input('Enter y coordinate:', min_value=0, max_value=img.height-1, value=int(img.height/2), step=1)

  # Display the original image
  st.image(img, caption='Original Image')

  x, y = int(x), int(y)
  # 获取种子点的灰度值
  seed_value = gray_img[y, x]
  st.write(f'The gray level of the seed point is: {seed_value}')

  # 获取用户输入的增长准则
  threshold = st.number_input('Enter growth criterion:', min_value=0, max_value=255, value=50, step=1)


  # 在主程序中使用区域增长算法
  gray_img = region_growing(gray_img, (x, y), threshold) # type: ignore

  # 更新Plotly图像
  fig = go.Figure(data=go.Heatmap(z=gray_img, colorscale='gray', showscale=False))

  # 在图像上添加十字线
  fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=gray_img.shape[0], line=dict(color="Red", width=2))
  fig.add_shape(type="line", x0=0, y0=y, x1=gray_img.shape[1], y1=y, line=dict(color="Red", width=2))

  # 自动调整图像大小以适应窗口宽度
  fig.update_layout(autosize=True)
  # Set the layout to keep the original aspect ratio
  #fig.update_layout(
  #    autosize=False,
  #    width=img.width,
  #    height=img.height,
  #)
  st.plotly_chart(fig)

  # enter 模糊比参数b=光学/SAR
  b = st.number_input('Enter the fuzzy ratio parameter b:', min_value=1.0, max_value=10.0, value=3.0, step=0.1)

  # 计算带宽omega
  omega = 5.0*np.sqrt(gray_img.shape[0] * gray_img.shape[1]) /(b)

  #original_picture = gray_img.copy()

  # 生成一个与图像大小相同的随机相位数组
  theta = np.random.uniform(0, 2*np.pi, gray_img.shape)

  # 对图像中的每个点乘以exp(j*theta)
  complex_img = gray_img * np.exp(1j * theta)
  # Apply the low-pass filter
  filtered_img = low_pass_filter(complex_img, int(omega))

  # Display the modified magnitude image
  fig = go.Figure(data=go.Heatmap(z=np.abs(filtered_img), colorscale='gray', showscale=False))
  fig.update_layout(autosize=True)
  st.plotly_chart(fig)

  fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),  # Set all margins to 0
    xaxis=dict(showgrid=False, zeroline=False, visible=False),  # Hide x-axis lines, ticks, and labels
    yaxis=dict(showgrid=False, zeroline=False, visible=False)  # Hide y-axis lines, ticks, and labels
  )
  # Save the figure without borders
  fig.write_image("./assets/image_without_borders.png")

def plot_difference(original_picture, picture):
    # Compute the absolute difference
    difference = np.abs(original_picture.astype(int) - picture.astype(int))

    # Convert the difference to uint8
    difference = difference.astype(np.uint8)

    # Create the x, y, and z coordinate arrays
    y, x = np.mgrid[:difference.shape[0], :difference.shape[1]]
    z = difference

    # Create a 3D surface plot
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

    return fig
# Create a 3D surface plot
#fig = plot_difference(original_picture, np.abs(filtered_img))

# Update layout options
#fig.update_layout(title='灰度差异的3D图像表示', autosize=False,
#                  width=500, height=500,
#                  margin=dict(l=65, r=50, b=65, t=90))

# Display the figure
#st.plotly_chart(fig)