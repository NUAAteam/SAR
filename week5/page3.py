import streamlit as st
from simulate import simulate
from SAR import sar
def page3():
    st.title("打击目标上传与选择")
    uploaded_files = st.file_uploader("上传图片", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'], help="一次性上传多张图片")

    if uploaded_files:
        # 显示缩略图
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, caption=uploaded_file.name, width=100)

        # 创建文件名到UploadedFile对象的映射
        file_name_to_object = {uploaded_file.name: uploaded_file for uploaded_file in uploaded_files}

        # 使用文件名列表填充选择框
        selected_file_name = st.selectbox("选择图片", options=list(file_name_to_object.keys()))

        # 从映射中获取选中的UploadedFile对象
        selected_file = file_name_to_object[selected_file_name]

        # 选择操作
        selected_action = st.selectbox("选择操作", ["请选择操作", "高分辨率SAR图像仿真", "图像打击效果仿真"])

        if selected_action == "高分辨率SAR图像仿真":
            sar(selected_file)
        elif selected_action == "图像打击效果仿真":
            simulate(selected_file)

