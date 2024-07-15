from simulate import simulate
from SAR import sar
import streamlit as st
def main():
    # 创建侧边栏选择框
  page = st.sidebar.selectbox("选择你的界面", [
    "主界面",
    "图像打击效果仿真",
    "高分辨率SAR图像仿真"
    "打击目标"
    ])

  if page == "主界面":
      # 主界面内容
      st.title("欢迎来到SAR图像仿真系统")

      #TODO 在这里写主界面的内容,应该是项目简介,使用说明等等

      st.write("请在侧边栏选择您想要查看的页面")

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

if __name__ == "__main__":
    main()