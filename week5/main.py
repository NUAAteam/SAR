from simulate import simulate
from page import page1
import streamlit as st
import io
def main():
    # 创建侧边栏选择框
    page = st.sidebar.selectbox("选择你的界面", [
        "进行仿真实验",
        "下载仿真实验结果"
    ])

    if page == "进行仿真实验":
        st.title("欢迎来到SAR图像仿真实验系统")
        #TODO 添加系统介绍
        page1()


    elif page == "下载仿真实验结果":
        st.title("下载仿真实验结果")
        # 假设simulate()返回处理后的图片字节流或路径
        result_image = simulate()
        if result_image:
            # 如果返回的是路径，需要读取图片到字节流
            if isinstance(result_image, str):
                with open(result_image, "rb") as file:
                    bytes_data = file.read()
            else:
                bytes_data = result_image
            st.download_button("下载仿真结果", bytes_data, "simulate_result.jpg", "image/jpeg")


if __name__ == "__main__":
    main()
