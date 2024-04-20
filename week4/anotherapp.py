import cv2
import streamlit as st
import draw  # import my module
import numpy as np

def main():
  st.title('高分辨率 SAR 图像打击效果评估')

  # Create sliders
  dm = st.slider('dm', min_value=0.0, max_value=2.0, value=1.0, step=0.1)
  dn = st.slider('dn', min_value=0.0, max_value=2.0, value=1.0,step=0.1)
  ic = st.slider('ic', min_value=0, max_value=100, value=50)
  jc = st.slider('jc', min_value=0, max_value=100, value=50)
  k = st.slider('k', min_value=0, max_value=3000, value=500)
  sigma = st.slider('sigma', min_value=0.0, max_value=3.0, value=1.0,step=0.1)

  # Generate the figure
  #todo 读取图片 from browser
  #picture=cv2.imread('week4/assets/nuaa_sar.jpg',cv2.IMREAD_GRAYSCALE)
  # Read the image from the browser
  uploaded_file = st.file_uploader("Choose an image...", type="jpg")
  if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    picture = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
  else:
    picture = cv2.imread('week4/assets/nuaa_sar.jpg', cv2.IMREAD_GRAYSCALE)

  fig = draw.draw_many_splinter(dm, dn, ic, jc, k, sigma,picture)

  # Display the figure
  st.plotly_chart(fig)

if __name__ == '__main__':
  main()