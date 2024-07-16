from simulate import simulate
from SAR import sar
import streamlit as st
import io
def main():
    page = st.sidebar.selectbox("选择你的界面", [
        "主界面",
        "图像打击效果仿真",
        "高分辨率SAR图像仿真",
        "打击目标"
    ])

    if page == "主界面":
        st.title("欢迎来到SAR图像仿真系统")
        #TODO 添加系统介绍
        st.write("请在侧边栏选择您想要查看的页面")

    elif page == "图像打击效果仿真":
        st.title("图像打击效果仿真")
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

    elif page == "高分辨率SAR图像仿真":
        st.title("高分辨率SAR图像仿真")
        # 假设sar()返回处理后的图片字节流或路径
        result_image = sar()
        if result_image:
            # 如果返回的是路径，需要读取图片到字节流
            if isinstance(result_image, str):
                with open(result_image, "rb") as file:
                    bytes_data = file.read()
            else:
                bytes_data = result_image
            st.download_button("下载SAR仿真结果", bytes_data, "sar_result.jpg", "image/jpeg")

    elif page == "打击目标":
        st.title("打击目标")
        uploaded_files = st.file_uploader("上传图片", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.image(uploaded_file, caption=uploaded_file.name, width=100)
            selected_action = st.selectbox("选择操作", ["请选择操作", "高分辨率SAR图像仿真", "图像打击效果仿真"])
            # 根据选择的操作执行相应函数并提供下载功能，这里省略了具体实现细节

if __name__ == "__main__":
    main()
