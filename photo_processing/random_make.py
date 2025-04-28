import cv2
import os
import random
import numpy as np

def add_multiple_patches_to_background(background_path, img_folder, num_patches=5):
    background = cv2.imread(background_path)

    # 获取背景图片的大小
    bg_height, bg_width, _ = background.shape

    # 获取文件夹中的所有图片路径
    img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(('.png', '.jpg', '.bmp'))]

    if not img_files:
        print(f"文件夹 {img_folder} 中没有找到图片！")
        return

    # 存储已放置的区域
    placed_regions = []

    def is_overlapping(x, y, width, height):
        """检查新区域是否与已放置的区域重叠"""
        for px, py, pw, ph in placed_regions:
            if not (x + width <= px or px + pw <= x or y + height <= py or py + ph <= y):
                return True
        return False

    for _ in range(num_patches):
        for _ in range(100):  # 尝试最多100次找到一个不重叠的位置
            # 随机选择一张图片
            img_path = random.choice(img_files)
            img = cv2.imread(img_path)

            if img is None:
                print(f"无法读取图片：{img_path}")
                continue

            img_height, img_width, _ = img.shape

            # 随机生成一个合适的位置
            random_x = random.randint(0, bg_width - img_width)
            random_y = random.randint(0, bg_height - img_height)

            # 检查是否与已放置的区域重叠
            if not is_overlapping(random_x, random_y, img_width, img_height):
                # 放置小图片
                background[random_y:random_y + img_height, random_x:random_x + img_width] = img
                placed_regions.append((random_x, random_y, img_width, img_height))
                break

    # 对生成的图像进行平滑处理（高斯模糊）
    smoothed_background = cv2.GaussianBlur(background, (15, 15), 0)

    # 保存平滑处理后的图像
    output_path = "photo_processing/output_with_multiple_patches_smoothed.bmp"
    cv2.imwrite(output_path, smoothed_background)
    print(f"Smoothed image with multiple patches saved as {output_path}")

# 使用示例
background_path = "photo_processing/Background3.bmp"  # 替换为背景图片路径
img_folder = "photo_processing/qipao3"  # 替换为包含小图片的文件夹路径
add_multiple_patches_to_background(background_path, img_folder, num_patches=50)