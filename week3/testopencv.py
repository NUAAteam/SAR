# app.py
import cv2
import numpy as np
import plotly.graph_objs as go
import io


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from layout import layout
import draw  # import my module

app = dash.Dash(__name__)

app.layout = eval(layout)

#todo1: 读入图像数据
picture=cv2.imread('week3\\assets\\nuaa_sar.jpg',cv2.IMREAD_GRAYSCALE)
print(picture)