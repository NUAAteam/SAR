import streamlit as st
from simulate import simulate
from SAR import sar
import tempfile
import os
import plotly.io as pio
import tempfile
from PIL import Image
import numpy as np

def image_path_to_ndarray(image_path):
    # 使用Pillow打开图像文件
    image = Image.open(image_path)
    # 将图像转换为numpy数组
    image_array = np.array(image)
    return image_array
def save_plotly_fig_as_image(fig):
    # 创建一个临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png', mode='w+b')
    # 将Plotly图形保存为PNG图像到临时文件
    pio.write_image(fig, temp_file.name)
    # 返回临时文件的路径
    return temp_file.name
def save_simulation_results_to_tempdir(simulation_results):
    # 创建一个临时目录
    temp_dir = tempfile.mkdtemp()
    # 保存每个仿真结果到临时目录
    for i, simulation_result in enumerate(simulation_results):
        image = Image.fromarray(simulation_result)
        temp_file_path = os.path.join(temp_dir, f'simulation_{i}.jpeg')
        # 使用Pillow的save方法保存图像
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(temp_file_path, 'JPEG')
    # 返回临时目录的路径
    return temp_dir
def page1():
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

        simulate_results = []
        if selected_action == "高分辨率SAR图像仿真":
            fig = sar(selected_file)
            st.write("最终仿真效果如下：")
            # 将Plotly图形转换为图像并获取图像文件路径
            image_path = save_plotly_fig_as_image(fig)
            # 使用Streamlit显示图像
            st.image(image_path, caption='处理后图像', use_column_width=True)
            image_array=image_path_to_ndarray(image_path)
            simulate_results.append(image_array)
        elif selected_action == "图像打击效果仿真":
            picture=simulate(selected_file)
            st.write("最终仿真效果如下：")
            st.image(picture, caption='处理后图像', use_column_width=True)
            simulate_results.append(picture)
        # 保存仿真结果到临时目录
        temp_dir = save_simulation_results_to_tempdir(simulate_results)
        return temp_dir

