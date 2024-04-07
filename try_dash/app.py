from dash import Dash,html,dcc,callback,Output,Input
app = Dash(__name__)

app.layout = html.Div([
  dcc.Slider(-4,10,2,value=2),
])

if __name__ == '__main__':
  app.run(debug=True)