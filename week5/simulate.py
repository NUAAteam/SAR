import cv2
import streamlit as st
import draw  # import my module
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
from noise import pnoise2  # 导入柏林噪声函数x

def plot_difference(original_picture, picture):
    # Compute the absolute difference
    difference = np.abs(original_picture.astype(int) - picture.astype(int))

    # Convert the difference to uint8
    difference = difference.astype(np.uint8)

    # Create the x, y, and z coordinate arrays
    y, x = np.mgrid[:difference.shape[0], :difference.shape[1]]
    z = difference

    # Apply Perlin noise to simulate more natural effects
    scale = 0.1  # Scale of the noise
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            z[i, j] += pnoise2(i * scale, j * scale) * 255  # Adjust intensity of the effect


    # Create a 3D surface plot
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

    return fig
def simulate(uploaded_file=None):
  # Create sliders
  dm = st.slider('横向打击分辨度', min_value=0.0, max_value=2.0, value=1.0, step=0.1)
  dn = st.slider('纵向打击分辨度', min_value=0.0, max_value=2.0, value=1.0,step=0.1)
  col1, col2 = st.columns(2)
  # Create sliders in each column
  ic = col1.number_input('原爆点X轴坐标', min_value=0, max_value=10000, value=150)
  jc = col2.number_input('原爆点Y轴坐标', min_value=0, max_value=10000, value=150)
  k = st.slider('打击密度', min_value=0, max_value=5000, value=1500)
  sigma = st.slider('毁伤程度', min_value=0.01, max_value=5.0, value=1.0,step=0.1)

  # Generate the figure


  # Read the image from the browser
  #uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

  if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    picture = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
  else:
    imgpath=os.path.abspath('./assets/nuaa_sar.jpg')
    picture = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)


  st.image(picture, caption='原始图像', use_column_width=True)
  picture=draw.process_picture(dm, dn, ic, jc, k, sigma, picture)
  st.image(picture, caption='处理后图像', use_column_width=True)

  # Create a 3D surface plot
  #fig = plot_difference(original_picture, picture)

  # Update layout options
  #fig.update_layout(title='灰度差异的3D图像表示', autosize=False,
  #                width=500, height=500,
  #                margin=dict(l=65, r=50, b=65, t=90))
  # Display the figure
  #st.plotly_chart(fig)

  # Create a new figure and axes
  fig, ax = plt.subplots()
  # Display the image
  ax.imshow(picture, cmap='gray')
  # Set the labels for the x and y axes
  ax.set_xlabel('Pixel Scale X')
  ax.set_ylabel('Pixel Scale Y')
  # Set the x and y ticks to be every 50 pixels
  ax.set_xticks(np.arange(0, picture.shape[1], 150))
  ax.set_yticks(np.arange(0, picture.shape[0], 150))
  # Add a grid
  ax.grid(True, color='r', linestyle='-', linewidth=0.5)

  # Display the figure in Streamlit
  st.pyplot(fig)
  return picture


