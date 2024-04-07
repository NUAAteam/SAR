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
    fig = draw.draw_many_splinter(dm, dn, ic, jc, k, sigma)
    # Convert the figure to an image
    fig.write_image('temp.png')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0",port=5000)
