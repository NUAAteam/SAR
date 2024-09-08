# layout.py

layout = """
html.Div([
    html.Div([
        html.H1("高分辨率 SAR 图像打击效果评估", style={'textAlign': 'center'}),
        html.Label('dm:'),
        dcc.Slider(
            id='dm-slider',
            min=0.1,
            max=2,
            step=0.1,
            value=1,
        ),
        html.Label('dn:'),
        dcc.Slider(
            id='dn-slider',
            min=0.1,
            max=2,
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
        max=3,
        step=0.1,
        value=1,
        ),
        dcc.Graph(id='graph'),
    ], style={'width': '100%', 'display': 'inline-block'})
])
"""