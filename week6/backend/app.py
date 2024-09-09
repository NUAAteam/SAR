from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import cv2
import numpy as np
import base64
from io import BytesIO
from simulation import simulate
from PIL import Image
import io
from SAR import sar
from damage_assessment_with_registration import damage_assessment, calculate_damage_statistics, visualize_damage

app = Flask(__name__)
CORS(app)

# 全局变量来存储图像和统计数据
original_image = None
simulated_image = None
damage_statistics = None

@app.route('/simulate', methods=['POST'])
def api_simulate():
    # 获取上传的图片和参数
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    params = request.form.to_dict()

    # 读取图片
    image_data = file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    original_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if original_image is None:
        return jsonify({'error': 'Failed to decode image'}), 400

    # 调用模拟函数
    simulated_image = simulate(original_image.copy(), params)

    # 将结果图片转换为灰度图像
    simulated_image_gray = cv2.cvtColor(simulated_image, cv2.COLOR_BGR2GRAY)

    # 将结果图片转换为base64编码
    _, buffer = cv2.imencode('.png', simulated_image_gray)
    img_str = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'image': img_str})

@app.route('/sar_simulate', methods=['POST'])
def sar_simulate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    file = request.files['image']
    image_data = file.read()

    b = float(request.form['b'])
    threshold = int(request.form['threshold'])
    x = int(request.form['x'])
    y = int(request.form['y'])

    # 调用SAR仿真函数
    result_img_data = sar(image_data, x, y, threshold, b)

    # 将图像数据转换为灰度图
    result_img_gray = cv2.cvtColor(result_img_data, cv2.COLOR_BGR2GRAY)

    # 将图像数据转换为base64编码的字符串
    _, buffer = cv2.imencode('.png', result_img_gray)
    img_str = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'image': img_str})

@app.route('/assess_damage', methods=['POST'])
def assess_damage():
    if 'original_image' not in request.files or 'simulated_image' not in request.files:
        return jsonify({'error': 'Both original and simulated images are required'}), 400

    original_file = request.files['original_image']
    simulated_file = request.files['simulated_image']

    # 读取原始图像和模拟图像
    original_image = cv2.imdecode(np.frombuffer(original_file.read(), np.uint8), cv2.IMREAD_COLOR)
    simulated_image = cv2.imdecode(np.frombuffer(simulated_file.read(), np.uint8), cv2.IMREAD_COLOR)

    if original_image is None or simulated_image is None:
        return jsonify({'error': 'Failed to decode images'}), 400

    # 执行毁伤评估
    damage_levels, diff_image = damage_assessment(original_image, simulated_image)

    # 计算毁伤统计
    damage_counts, damage_statistics = calculate_damage_statistics(damage_levels)

    # 可视化结果
    result_image = visualize_damage(simulated_image, damage_levels)

    # 将结果图像转换为字节流
    _, buffer = cv2.imencode('.png', result_image)
    img_byte_arr = BytesIO(buffer)

    # 发送图像和统计数据
    return jsonify({
        'image': base64.b64encode(img_byte_arr.getvalue()).decode('utf-8'),
        'damage_statistics': damage_statistics
    })

@app.route('/get_damage_statistics', methods=['GET'])
def get_damage_statistics():
    global damage_statistics
    if damage_statistics is None:
        return jsonify({'error': 'No damage statistics available'}), 400
    return jsonify({'damage_statistics': damage_statistics})

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/hello')
def hello():
    return jsonify(message="Hello from the backend!")

if __name__ == '__main__':
    app.run(debug=True)