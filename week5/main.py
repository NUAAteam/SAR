from simulate import simulate
from page1 import page1
from page2 import page2
import streamlit as st
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
        #TODO 添加下载界面
        page2()


if __name__ == "__main__":
    main()
