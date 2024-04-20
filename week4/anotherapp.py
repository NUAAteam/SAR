import cv2
import streamlit as st
import draw  # import my module

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
  picture=cv2.imread('week4/assets/nuaa_sar.jpg',cv2.IMREAD_GRAYSCALE)
  fig = draw.draw_many_splinter(dm, dn, ic, jc, k, sigma,picture)

  # Display the figure
  st.plotly_chart(fig)

if __name__ == '__main__':
  main()