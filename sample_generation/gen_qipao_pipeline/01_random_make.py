import cv2
import os
import random
import numpy as np
import time
import argparse
from datetime import datetime

def add_multiple_patches_to_background(background_path, img_folder, num_patches=5, output_dir="sample_generation/output"):
    background = cv2.imread(background_path)

    # 获取背景图片的大小
    bg_height, bg_width, _ = background.shape

    # 获取文件夹中的所有图片路径
    img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(('.png')) and not f.endswith(('_target.png'))]

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

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 使用当前时间戳作为文件名，精确到毫秒
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = os.path.join(output_dir, f"{timestamp}_qipao.png")
    
    cv2.imwrite(output_path, background)
    print(f"图像已保存为 {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='生成多组带气泡的背景图像')
    parser.add_argument('--runs', type=int, default=10, help='运行生成过程的次数')
    parser.add_argument('--patches', type=int, default=50, help='每张图像中的气泡数量')
    parser.add_argument('--background', type=str, default="sample_generation/Background.bmp", help='背景图像路径')
    parser.add_argument('--img_folder', type=str, default="sample_generation/qipao_final_matched", help='气泡图像文件夹路径')
    parser.add_argument('--output_dir', type=str, default="sample_generation/output", help='输出目录')
    
    args = parser.parse_args()
    
    generated_files = []
    for i in range(args.runs):
        print(f"正在生成第 {i+1}/{args.runs} 张图像...")
        output_path = add_multiple_patches_to_background(
            args.background, 
            args.img_folder, 
            num_patches=args.patches,
            output_dir=args.output_dir
        )
        generated_files.append(output_path)
    
    print(f"已成功生成 {len(generated_files)} 张图像:")
    for path in generated_files:
        print(f"  - {path}")

if __name__ == "__main__":
    main()