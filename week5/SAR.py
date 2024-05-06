import numpy as np
from scipy.signal import convolve
import matplotlib.pyplot as plt
import draw

# Load the picture
picture = ...

# Process the picture
backscatter_coefficients = draw.process_picture()

# 创建一个表示 SAR 成像系统的冲击响应函数的 numpy 数组
# 这个数组应该尽可能接近一个 delta 函数
impulse_response = np.zeros_like(backscatter_coefficients)
impulse_response[backscatter_coefficients.shape[0] // 2, backscatter_coefficients.shape[1] // 2] = 1

# 使用 convolve 函数来模拟卷积
sar_image = convolve(backscatter_coefficients, impulse_response, mode='same')

# 显示 SAR 图像
plt.imshow(sar_image, cmap='gray')
plt.show()

#如何选取机场或者金属区域？ps？