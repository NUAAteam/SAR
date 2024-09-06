from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from simulation import simulate  # 导入您的模拟函数

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/simulate', methods=['POST'])
def api_simulate():
    # 获取上传的图片和参数
    file = request.files['image']
    params = request.form.to_dict()

    # 读取图片
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    # 调用您的模拟函数
    result = simulate(img, params)

    # 将结果图片转换为base64编码
    _, buffer = cv2.imencode('.png', result)
    img_str = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'image': img_str})

if __name__ == '__main__':
    app.run(debug=True)