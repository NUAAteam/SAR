import streamlit as st
from simulate import simulate
from SAR import sar
def page3():
      st.title("打击目标")
      uploaded_files = st.file_uploader("上传图片", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'], help="一次性上传多张图片")

      if uploaded_files:
        for uploaded_file in uploaded_files:
              st.image(uploaded_file, caption=uploaded_file.name, width=100)

        selected_action = st.selectbox("选择操作", ["请选择操作", "高分辨率SAR图像仿真", "图像打击效果仿真"])

        if selected_action == "高分辨率SAR图像仿真":
              sar()
        elif selected_action == "图像打击效果仿真":
              simulate()

