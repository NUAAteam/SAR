import numpy as np
from PIL import Image
from scipy import signal
import io

def region_growing(img, seed, threshold):
    mask = np.zeros(img.shape, dtype=bool)
    seed_value = int(img[seed])
    mask[seed] = True
    neighbors = [(0,1), (1,0), (0,-1), (-1,0)]
    stack = [seed]
    while stack:
        x, y = stack.pop()
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < img.shape[0] and 0 <= ny < img.shape[1]:
                if not mask[nx, ny] and abs(int(img[nx, ny]) - seed_value) <= threshold:
                    mask[nx, ny] = True
                    stack.append((nx, ny))
    return mask

def sar(image_data, x, y, threshold, b):
    # 将图像数据转换为numpy数组
    img = Image.open(io.BytesIO(image_data)).convert('L')
    img_array = np.array(img)

    # 应用区域增长算法
    mask = region_growing(img_array, (y, x), threshold)

    # 将选中区域设为黑色，其他区域保持不变
    img_array[mask] = 0

    # 计算带宽omega
    omega = 5.0 * np.sqrt(img_array.shape[0] * img_array.shape[1]) / b

    # 生成随机相位
    theta = np.random.uniform(0, 2*np.pi, img_array.shape)
    complex_img = img_array * np.exp(1j * theta)

    # 应用低通滤波器
    rows, cols = img_array.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), dtype=bool)
    y, x = np.ogrid[-crow:rows-crow, -ccol:cols-ccol]
    mask = x*x + y*y <= omega*omega
    f = np.fft.fft2(complex_img)
    f_shifted = np.fft.fftshift(f)
    f_filtered = f_shifted * mask
    f_filtered_shifted = np.fft.ifftshift(f_filtered)
    filtered_img = np.fft.ifft2(f_filtered_shifted)

    # 计算幅度
    result = np.abs(filtered_img)

    # 归一化结果到0-255范围
    result = ((result - result.min()) / (result.max() - result.min()) * 255).astype(np.uint8)

    # 创建PIL图像
    result_img = Image.fromarray(result)

    # 将图像转换为字节流
    img_byte_arr = io.BytesIO()
    result_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return result