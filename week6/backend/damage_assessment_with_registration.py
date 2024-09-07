import cv2
import numpy as np
from scipy.ndimage import gaussian_filter

def damage_assessment(img1, img2, window_size=9):
    # 确保两幅图像大小相同
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # 转换为灰度图像并确保数据类型为float32
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY).astype(np.float32)

    # 计算图像差异
    diff = np.abs(gray1 - gray2)

    # 使用高斯滤波器平滑差异图像
    smoothed_diff = gaussian_filter(diff, sigma=window_size/3)

    # 归一化差异图像
    normalized_diff = (smoothed_diff - np.min(smoothed_diff)) / (np.max(smoothed_diff) - np.min(smoothed_diff))

    # 应用非线性变换以增强小差异
    enhanced_diff = np.power(normalized_diff, 0.5)

    # 设置毁伤等级的阈值
    thresholds = [0.2, 0.4, 0.6, 0.8]

    # 创建毁伤等级图像
    damage_levels = np.zeros_like(enhanced_diff, dtype=np.uint8)
    for i, threshold in enumerate(thresholds, start=1):
        damage_levels[enhanced_diff >= threshold] = i

    # 应用形态学操作以平滑结果
    kernel = np.ones((3, 3), np.uint8)
    damage_levels = cv2.morphologyEx(damage_levels, cv2.MORPH_CLOSE, kernel)

    # 打印调试信息
    unique, counts = np.unique(damage_levels, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"Level {u}: {c} pixels")

    return damage_levels, enhanced_diff

def calculate_damage_statistics(damage_levels):
    total_pixels = damage_levels.size
    damage_counts = {
        0: np.sum(damage_levels == 0),
        1: np.sum(damage_levels == 1),
        2: np.sum(damage_levels == 2),
        3: np.sum(damage_levels == 3),
        4: np.sum(damage_levels == 4)
    }
    damage_percentages = {level: count / total_pixels * 100 for level, count in damage_counts.items()}
    return damage_counts, damage_percentages

def visualize_damage(original_image, damage_levels):
    # 创建一个彩色掩码来表示不同的毁伤等级
    color_mask = np.zeros_like(original_image)
    color_mask[damage_levels == 1] = [0, 255, 255]   # 黄色：1级毁伤
    color_mask[damage_levels == 2] = [0, 128, 255]   # 橙色：2级毁伤
    color_mask[damage_levels == 3] = [0, 0, 255]     # 红色：3级毁伤
    color_mask[damage_levels == 4] = [255, 0, 255]   # 紫色：4级毁伤

    # 创建一个半透明的黑色背景
    dark_background = np.zeros_like(original_image)
    result = cv2.addWeighted(original_image, 0.7, dark_background, 0.3, 0)

    # 将毁伤区域叠加到结果图像上
    alpha = 0.6  # 透明度
    mask = damage_levels > 0
    result[mask] = cv2.addWeighted(result[mask], 1 - alpha, color_mask[mask], alpha, 0)

    # 应用锐化滤波器
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    result = cv2.filter2D(result, -1, kernel)

    return result

if __name__ == "__main__":
    image1_path = r"C:\Users\Lenovo\Desktop\SAR\week6\backend\img\111.jpg"
    image2_path = r"C:\Users\Lenovo\Desktop\SAR\week6\backend\img\222.png"

    # 读取图像
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # 执行毁伤评估
    damage_levels, diff_image = damage_assessment(img1, img2)

    # 计算毁伤统计
    damage_counts, damage_percentages = calculate_damage_statistics(damage_levels)

    # 可视化结果
    result = visualize_damage(img2, damage_levels)

    # 打印毁伤统计
    print("毁伤统计：")
    for level, percentage in damage_percentages.items():
        print(f"{level}级毁伤: {percentage:.2f}%")

    # 显示结果
    cv2.imshow("Original Image (Before)", img1)
    cv2.imshow("Original Image (After)", img2)
    cv2.imshow("Difference Image", diff_image.astype(np.uint8))
    cv2.imshow("Damage Assessment Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
