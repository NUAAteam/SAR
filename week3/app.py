# app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import draw  # import the module

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Slider(
        id='dm-slider',
        min=0.1,
        max=1,
        step=0.1,
        value=1,
    ),
    dcc.Slider(
        id='dn-slider',
        min=0.1,
        max=1,
        step=0.1,
        value=1,
    ),
    dcc.Slider(
        id='k-slider',
        min=100,
        max=1000,
        step=100,
        value=500,
    ),
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
     Input('k-slider', 'value'),
     Input('sigma-slider', 'value')]
)
def update_figure(dm, dn, k, sigma):
    ic = 50
    jc = 50
    fig = draw.draw_many_points(dm, dn, ic, jc, k, sigma)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
