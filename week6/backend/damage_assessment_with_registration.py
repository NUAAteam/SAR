import cv2
import numpy as np
from scipy.ndimage import uniform_filter

def register_images(img1, img2):
    # 转换为灰度图像
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 创建 SIFT 对象并检测关键点
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # 使用 FLANN 匹配器
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # 应用比率测试
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # 确保有足够的好匹配点
    MIN_MATCH_COUNT = 10
    if len(good_matches) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算仿射变换矩阵
        M, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts)

        # 应用仿射变换
        h, w = img1.shape[:2]
        aligned_img = cv2.warpAffine(img1, M, (w, h))
    else:
        print(f"Not enough good matches are found - {len(good_matches)}/{MIN_MATCH_COUNT}")
        aligned_img = img1

    return aligned_img

def damage_assessment(img1, img2, window_size=3):
    # 确保两幅图像大小相同
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # 转换为灰度图像
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 使用均值滤波器计算窗口均值
    img1_mean = uniform_filter(gray1, size=window_size)
    img2_mean = uniform_filter(gray2, size=window_size)

    # 计算差值图像
    diff_image = np.abs(img1_mean - img2_mean)

    # 计算差值图像的标准差
    sigma = np.std(diff_image)

    # 创建毁伤等级图像
    damage_levels = np.zeros_like(diff_image, dtype=np.uint8)

    # 应用毁伤评估准则
    damage_levels[(diff_image >= sigma) & (diff_image < 1.5*sigma)] = 1
    damage_levels[(diff_image >= 1.5*sigma) & (diff_image < 2*sigma)] = 2
    damage_levels[(diff_image >= 2*sigma) & (diff_image < 2.5*sigma)] = 3
    damage_levels[diff_image >= 2.5*sigma] = 4

    return damage_levels, diff_image

def visualize_damage(original_image, damage_levels):
    # 创建一个彩色掩码来表示不同的毁伤等级
    color_mask = np.zeros_like(original_image)
    color_mask[damage_levels == 1] = [0, 255, 255]   # 亮黄色：1级毁伤
    color_mask[damage_levels == 2] = [0, 128, 255]   # 橙色：2级毁伤
    color_mask[damage_levels == 3] = [0, 0, 255]     # 红色：3级毁伤
    color_mask[damage_levels == 4] = [255, 0, 255]   # 洋红色：4级毁伤

    # 创建一个半透明的黑色背景
    dark_background = np.zeros_like(original_image)
    result = cv2.addWeighted(original_image, 0.3, dark_background, 0.7, 0)

    # 将毁伤区域叠加到结果图像上
    result[damage_levels > 0] = color_mask[damage_levels > 0]

    return result

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

if __name__ == "__main__":
    image1_path = r"C:\Users\Lenovo\Desktop\SAR\week6\backend\img\111.jpg"
    image2_path = r"C:\Users\Lenovo\Desktop\SAR\week6\backend\img\222.png"

    # 读取图像
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # 图像配准
    aligned_img1 = register_images(img1, img2)

    # 执行毁伤评估
    damage_levels, diff_image = damage_assessment(aligned_img1, img2, window_size=3)

    # 可视化结果
    result = visualize_damage(img2, damage_levels)

    # 计算毁伤统计
    damage_counts, damage_percentages = calculate_damage_statistics(damage_levels)

    # 显示结果
    cv2.imshow("Original Image (Before)", img1)
    cv2.imshow("Original Image (After)", img2)
    cv2.imshow("Aligned Image", aligned_img1)
    cv2.imshow("Difference Image", diff_image.astype(np.uint8))
    cv2.imshow("Damage Assessment Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 打印毁伤统计
    print("毁伤统计：")
    print(f"无毁伤: {damage_percentages[0]:.2f}%")
    print(f"1级毁伤: {damage_percentages[1]:.2f}%")
    print(f"2级毁伤: {damage_percentages[2]:.2f}%")
    print(f"3级毁伤: {damage_percentages[3]:.2f}%")
    print(f"4级毁伤: {damage_percentages[4]:.2f}%")
