import cv2
import streamlit as st
import draw  # import my module
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def main():
  st.title('高分辨率 SAR 图像打击效果评估')

  # Create sliders
  dm = st.slider('横向打击精度', min_value=0.0, max_value=2.0, value=1.0, step=0.1)
  dn = st.slider('纵向打击精度', min_value=0.0, max_value=2.0, value=1.0,step=0.1)
  col1, col2 = st.columns(2)
  # Create sliders in each column
  ic = col1.number_input('原爆点X轴坐标', min_value=0, max_value=10000, value=150)
  jc = col2.number_input('原爆点Y轴坐标', min_value=0, max_value=10000, value=150)
  k = st.slider('打击密度', min_value=0, max_value=5000, value=1500)
  sigma = st.slider('毁伤程度', min_value=0.01, max_value=5.0, value=1.0,step=0.1)

  # Generate the figure
  #todo 读取图片 from browser
  #picture=cv2.imread('week4/assets/nuaa_sar.jpg',cv2.IMREAD_GRAYSCALE)
  # Read the image from the browser
  uploaded_file = st.file_uploader("Choose an image...", type="jpg")
  if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    picture = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    #picture = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
  else:
    picture = cv2.imread('week4/assets/nuaa_sar.jpg', cv2.IMREAD_GRAYSCALE)

  #fig = draw.draw_many_splinter(dm, dn, ic, jc, k, sigma,picture)
  st.image(picture, caption='原始图像', use_column_width=True)
  original_picture = picture.copy()
  picture=draw.process_picture(dm, dn, ic, jc, k, sigma, picture)
  st.image(picture, caption='处理后图像', use_column_width=True)

# Compute the absolute difference
  difference = np.abs(original_picture.astype(int) - picture.astype(int))

# Convert the difference to uint8
  difference = difference.astype(np.uint8)

# Create the x, y, and z coordinate arrays
  y, x = np.mgrid[:difference.shape[0], :difference.shape[1]]
  z = difference

# Create a 3D surface plot
  fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

# Update layout options
  fig.update_layout(title='灰度差异的3D图像表示', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

# Display the figure
  st.plotly_chart(fig)

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

if __name__ == '__main__':
  main()