import cv2
import numpy as np
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

    # 随机从边框像素中选取值构建背景图
    R_sampled = np.random.choice(R, size=(height, width)).astype(np.uint8)
    G_sampled = np.random.choice(G, size=(height, width)).astype(np.uint8)
    B_sampled = np.random.choice(B, size=(height, width)).astype(np.uint8)

    # 合并通道(灰度图)
    generated_image = cv2.merge([R_sampled, R_sampled, R_sampled])

    # 保存生成的图像
    cv2.imwrite(output_path, generated_image)
    print(f"生成的图像已保存到：{output_path}")

# 使用示例
img_folder = "sample_generation_yuyan/yuyan_matched"  # 替换为包含图片的文件夹路径
output_path = "sample_generation_yuyan/Background_dis.bmp"  # 替换为输出图像路径
process_images_and_generate_sample(img_folder, output_path)