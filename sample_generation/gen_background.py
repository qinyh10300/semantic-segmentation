import cv2
import numpy as np
from scipy.stats import norm
import os

def process_images_and_generate_sample(img_folder, output_path, height=3648, width=5472):
    # 获取文件夹中的所有图片路径
    img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(('.png', '.jpg', '.bmp'))]

    if not img_files:
        print(f"文件夹 {img_folder} 中没有找到图片！")
        return

    # 存储所有图片的边框像素值
    all_border_pixels = []

    for img_path in img_files:
        # 读取图像
        image = cv2.imread(img_path)
        if image is None:
            print(f"无法读取图像：{img_path}")
            continue

        # 获取图像边框像素值
        border_pixels = []
        img_height, img_width, _ = image.shape

        # 提取边框像素值
        border_pixels.extend(image[0, :, :].tolist())  # 上边框
        border_pixels.extend(image[-1, :, :].tolist())  # 下边框
        border_pixels.extend(image[:, 0, :].tolist())  # 左边框
        border_pixels.extend(image[:, -1, :].tolist())  # 右边框

        all_border_pixels.extend(border_pixels)

    all_border_pixels = np.array(all_border_pixels)

    # 分离 R、G、B 通道
    R = all_border_pixels[:, 2]
    G = all_border_pixels[:, 1]
    B = all_border_pixels[:, 0]

    # 筛选 1%-99% 分位数范围内的值
    def filter_percentile(channel):
        lower = np.percentile(channel, 1)
        upper = np.percentile(channel, 99)
        return channel[(channel >= lower) & (channel <= upper)]

    R_filtered = filter_percentile(R)
    G_filtered = filter_percentile(G)
    B_filtered = filter_percentile(B)

    # 拟合高斯分布
    R_mean, R_std = norm.fit(R_filtered)
    G_mean, G_std = norm.fit(G_filtered)
    B_mean, B_std = norm.fit(B_filtered)

    print(f"R通道均值: {R_mean}, 标准差: {R_std}")
    print(f"G通道均值: {G_mean}, 标准差: {G_std}")
    print(f"B通道均值: {B_mean}, 标准差: {B_std}")

    # 生成指定大小的图像
    R_sampled = np.random.normal(R_mean, R_std, (height, width)).clip(0, 255).astype(np.uint8)
    G_sampled = np.random.normal(G_mean, G_std, (height, width)).clip(0, 255).astype(np.uint8)
    B_sampled = np.random.normal(B_mean, B_std, (height, width)).clip(0, 255).astype(np.uint8)

    # 合并通道
    generated_image = cv2.merge([B_sampled, G_sampled, R_sampled])

    # 保存生成的图像
    cv2.imwrite(output_path, generated_image)
    print(f"生成的图像已保存到：{output_path}")

# 使用示例
img_folder = "photo_processing/qipao3"  # 替换为包含图片的文件夹路径
output_path = "photo_processing/Background3.bmp"  # 替换为输出图像路径
process_images_and_generate_sample(img_folder, output_path)