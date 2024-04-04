from flask import Flask
import sys
sys.path.append("C:\\Users\\Lenovo\\Desktop\\SAR\\week1")
from new import draw_many_points
from new import draw_point
import matplotlib.pyplot as plt
import asyncio
import nest_asyncio
nest_asyncio.apply()


# 图像大小
width=10
height=10

# 间隔
dn=1
dm=1

# 中心点在图像中的位置(百分比)
ic=50
jc=50

# 打击参数
k=500
sigma=1

app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"
def draw():
  draw_many_points(width,height,dm, dn, ic, jc, k, sigma, draw_point)
  pass


@app.route("/status")
def status():
    return {"result": "OK - healthy"}

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3000)