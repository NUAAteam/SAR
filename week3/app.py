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
#todo2: 转换为SAR图像
@app.callback(
    Output('graph', 'figure'),
    [Input('dm-slider', 'value'),
     Input('dn-slider', 'value'),
     Input('ic-slider', 'value'),
     Input('jc-slider', 'value'),
     Input('k-slider', 'value'),
     Input('sigma-slider', 'value')]
)
def update_figure(dm, dn, ic, jc, k, sigma):
#todo1：图像与碎片融合
    fig = draw.draw_many_splinter(dm, dn, ic, jc, k, sigma, picture)
    # Convert the figure to an image
    #fig.write_image('temp.png')

    return fig

#opencv read image


if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0",port=5000)
