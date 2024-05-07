import cv2
from matplotlib import pyplot as plt

def main():
    # 读取图像
    img = cv2.imread('C:/Users/Lenovo/Desktop/SAR/week4/runway.jpg')
    if img is None:
        print("Error: Image not found.")
        return

    # 将BGR图像转换为RGB图像以便正确显示
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 转换为灰度图
    gray_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # 使用Canny算法进行边缘检测
    edges = cv2.Canny(gray_img, 100, 200)

    # 显示原图和边缘检测结果
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.imshow(img_rgb)
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(edges, cmap='gray')
    plt.title('Edge Detection')
    plt.axis('off')

    plt.show()

    # 用户选择像素
    print("Please click on the runway in the original image to select a pixel.")
    plt.imshow(img_rgb)
    point = plt.ginput(1)  # 让用户选择一个点
    plt.close()

    # 获取选定像素的坐标和值
    x, y = int(point[0][0]), int(point[0][1])
    selected_pixel_value = img_rgb[y, x]
    print(f"Selected pixel coordinates: ({x}, {y})")
    print(f"Selected pixel RGB value: {selected_pixel_value}")

if __name__ == '__main__':
    main()
