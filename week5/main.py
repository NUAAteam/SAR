from simulate import simulate
from SAR import sar
from page3 import page3
import streamlit as st
import io
def main():
    # 创建侧边栏选择框
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

    elif page == "图像打击效果仿真":
      # 第一个子页面内容
      st.title('图像打击效果仿真')
      # 在这里调用simulate函数来显示页面1的内容
      simulate()

    elif page == "高分辨率SAR图像仿真":
      # 第二个子页面内容
      st.title("高分辨率SAR图像仿真")
      sar()
    elif page == "打击目标":
      # 新增的打击目标功能区
      page3()

if __name__ == "__main__":
    main()
