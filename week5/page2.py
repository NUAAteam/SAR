import streamlit as st
def page2(storage_dir):
    if storage_dir is None:
        st.error("请先进行仿真实验")
    else:
        st.write(f"仿真实验结果存储在{storage_dir}")
        st.write("请点击以下链接下载：")
        st.markdown(f"[点击下载]({storage_dir}.zip)")