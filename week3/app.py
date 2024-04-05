# app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import draw  # import my module

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("高分辨率 SAR 图像打击效果评估", style={'textAlign': 'center'}),
    html.Label('dm:'),
    dcc.Slider(
        id='dm-slider',
        min=0.1,
        max=1,
        step=0.1,
        value=1,
    ),
    html.Label('dn:'),
    dcc.Slider(
        id='dn-slider',
        min=0.1,
        max=1,
        step=0.1,
        value=1,
    ),
    html.Label('ic:'),
    dcc.Slider(
        id='ic-slider',
        min=0,
        max=100,
        step=10,
        value=50,
    ),
    html.Label('jc:'),
    dcc.Slider(
        id='jc-slider',
        min=0,
        max=100,
        step=10,
        value=50,
    ),
    html.Label('k:'),
    dcc.Slider(
        id='k-slider',
        min=100,
        max=1000,
        step=100,
        value=500,
    ),
    html.Label('sigma:'),
    dcc.Slider(
        id='sigma-slider',
        min=1,
        max=10,
        step=1,
        value=1,
    ),
    dcc.Graph(
        id='graph'
    )
])

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
    fig = draw.draw_many_points(dm, dn, ic, jc, k, sigma)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
