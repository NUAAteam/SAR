import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from PIL import Image
import numpy as np
import cv2

# 加载图像
img_path = 'C:/Users/Lenovo/Desktop/SAR/week4/runway.jpg'
img = Image.open(img_path)
img_array = np.array(img)

# 转换为灰度图像
gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

# 创建Dash应用
app = dash.Dash(__name__)

app.layout = html.Div([
  dcc.Graph(
    id='image',
    figure={
      'data': [go.Heatmap(z=gray_img,
                colorscale='gray',
                showscale=False)],
      'layout': go.Layout(width=img.width, height=img.height, autosize=False)
    },
    config={
      'staticPlot': False,
      'displayModeBar': False
    }
  ),
  dcc.Input(id='threshold', type='number', value=20),
  html.Div(id='output')
])

@app.callback(
  Output('output', 'children'),
  [Input('image', 'clickData')],
  [State('threshold', 'value')]
)
def display_click_data(clickData, threshold):
  if clickData is None:
      return 'Click on the image to get pixel value.'

  # 获取点击位置的坐标
  x = int(clickData['points'][0]['x'])
  y = int(clickData['points'][0]['y'])

  # 区域增长算法
  visited = np.zeros_like(gray_img, dtype=np.bool_)
  dx = [-1, 0, 1, 0]
  dy = [0, 1, 0, -1]
  stack = [(x, y)]
  while stack:
      x, y = stack.pop()
      if not visited[y, x] and abs(gray_img[y, x] - gray_img[y, x]) <= threshold:
          visited[y, x] = True
          # 灰度反转
          gray_img[y, x] = 255 - gray_img[y, x]
          for i in range(4):
              nx, ny = x + dx[i], y + dy[i]
              if 0 <= nx < gray_img.shape[1] and 0 <= ny < gray_img.shape[0]:
                  stack.append((nx, ny))

  # 获取并返回像素值
  pixel_value = gray_img[y, x]
  return f'You clicked on pixel ({x}, {y}). Its value is {pixel_value}.'

if __name__ == '__main__':
    app.run_server(debug=True)