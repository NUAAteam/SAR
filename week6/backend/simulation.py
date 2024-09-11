import cv2
import numpy as np
import draw  # 您的自定义模块

def simulate(picture, params):
    # 从params中提取参数
    dm = float(params.get('dm', 1.0))
    dn = float(params.get('dn', 1.0))
    ic = int(params.get('ic', 150))
    jc = int(params.get('jc', 150))
    k = int(params.get('k', 1500))
    sigma = float(params.get('sigma', 1.0))

    # 处理图像
    processed_picture = draw.process_picture(dm, dn, ic, jc, k, sigma, picture)

    # 创建图表 (如果需要的话)
    # 注意: 这里我们不再使用 Streamlit 或 Matplotlib,
    # 因为我们现在是在后端处理,不需要直接显示图表
    # 如果需要图表数据,我们可以返回必要的数据供前端使用

    return processed_picture

# 如果需要额外的图表数据,可以添加一个新函数
def get_chart_data(picture):
    # 这里可以生成图表所需的数据
    # 例如:
    x_ticks = np.arange(0, picture.shape[1], 150)
    y_ticks = np.arange(0, picture.shape[0], 150)

    return {
        'x_ticks': x_ticks.tolist(),
        'y_ticks': y_ticks.tolist(),
        'width': picture.shape[1],
        'height': picture.shape[0]
    }

