import cv2
import os
import random
import numpy as np
import time
import argparse
from datetime import datetime

def add_multiple_patches_to_background(background_dir, img_folder, num_patches=5,
                                       output_dir="gen_qipao/output", output_target_dir="gen_qipao/output_target",
                                       index=0):
    # 获取背景文件夹中的所有图片路径
    background_files = [os.path.join(background_dir, f) for f in os.listdir(background_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    if not background_files:
        print(f"文件夹 {background_dir} 中没有找到背景图片！")
        return None, None
    
    # 随机选择一张背景图片
    background_path = random.choice(background_files)
    background = cv2.imread(background_path)
    
    if background is None:
        print(f"无法读取背景图片：{background_path}")
        return None, None
    
    print(f"已选择背景图片: {os.path.basename(background_path)}")

    # 获取背景图片的大小
    bg_height, bg_width, _ = background.shape
    
    # 创建一个全黑的目标掩码图像
    target_mask = np.zeros((bg_height, bg_width, 3), dtype=np.uint8)

    # 获取文件夹中的所有图片路径（不包括_target.png）
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

            # 获取对应的_target.png文件路径
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            target_file = os.path.join(img_folder, f"{base_name}_target.png")
            
            # 检查对应的目标文件是否存在
            if not os.path.exists(target_file):
                print(f"警告：未找到对应的目标文件： {target_file}")
                continue
                
            target_img = cv2.imread(target_file)

            if img is None or target_img is None:
                print(f"无法读取图片：{img_path} 或 {target_file}")
                continue

            img_height, img_width, _ = img.shape

            # 随机生成一个合适的位置
            random_x = random.randint(0, bg_width - img_width)
            random_y = random.randint(0, bg_height - img_height)

            # 检查是否与已放置的区域重叠
            if not is_overlapping(random_x, random_y, img_width, img_height):
                # 放置小图片到背景上
                background[random_y:random_y + img_height, random_x:random_x + img_width] = img
                # 放置对应的目标图片到黑色掩码图上
                target_mask[random_y:random_y + img_height, random_x:random_x + img_width] = target_img
                placed_regions.append((random_x, random_y, img_width, img_height))
                break

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_target_dir, exist_ok=True)
    
    # 使用当前时间戳作为文件名，精确到毫秒
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # output_path = os.path.join(output_dir, f"{timestamp}_qipao.png")
    # target_output_path = os.path.join(output_target_dir, f"{timestamp}_qipao_target.png")

    # 使用索引作为文件名
    output_path = os.path.join(output_dir, f"qipao_{index}.png")
    target_output_path = os.path.join(output_target_dir, f"qipao_target_{index}.png")
    
    cv2.imwrite(output_path, background)
    cv2.imwrite(target_output_path, target_mask)
    print(f"图像已保存为 {output_path}")
    print(f"目标掩码已保存为 {target_output_path}")
    return output_path, target_output_path

def main():
    parser = argparse.ArgumentParser(description='生成多组带气泡的背景图像')
    parser.add_argument('--runs', type=int, default=1000, help='运行生成过程的次数')
    parser.add_argument('--patches', type=int, default=50, help='每张图像中的气泡数量')
    parser.add_argument('--background_dir', type=str, default="/media/qinyh/KINGSTON/MetaData/background_data_resized/qipao", help='背景图像文件夹路径')
    parser.add_argument('--img_folder', type=str, default="/media/qinyh/KINGSTON/MetaData/qipao_data_matched", help='气泡图像文件夹路径')
    parser.add_argument('--output_dir', type=str, default="/media/qinyh/KINGSTON/GenData/qipao/qipao_random_make", help='输出目录')
    parser.add_argument('--output_target_dir', type=str, default="/media/qinyh/KINGSTON/GenData/qipao/qipao_target", help='输出目标目录')
    parser.add_argument('-i', '--index', type=int, default=0, help='开始索引')
    
    args = parser.parse_args()

    # 确保背景目录存在
    if not os.path.exists(args.background_dir):
        print(f"错误: 背景图片目录 '{args.background_dir}' 不存在！")
        return
    
    generated_files = []
    generated_targets = []
    for i in range(args.runs):
        print(f"正在生成第 {i+1}/{args.runs} 张图像...")
        if i < 200:
            args.patches = random.randint(5, 10)   # 少量
        elif i < 600:
            args.patches = random.randint(10, 35)   # 中等
        else:
            args.patches = random.randint(35, 50)   # 大量

        output_path, target_path = add_multiple_patches_to_background(
            args.background_dir, 
            args.img_folder, 
            num_patches=args.patches,
            output_dir=args.output_dir,
            output_target_dir=args.output_target_dir,
            index=args.index + i
        )
        generated_files.append(output_path)
        generated_targets.append(target_path)
    
    print(f"已成功生成 {len(generated_files)} 对图像:")
    for img_path, target_path in zip(generated_files, generated_targets):
        print(f"  - 图像: {img_path}")
        print(f"  - 目标: {target_path}")

if __name__ == "__main__":
    main()