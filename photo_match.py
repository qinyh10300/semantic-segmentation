#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filepath: /home/qinyh/codebase/semantic-segmentation/photo_match.py

import os
import shutil
import argparse
from pathlib import Path
from tqdm import tqdm

def match_and_save_photos(raw_folder, pse_folder, output_folder, target_folder, class_name):
    """
    在两个文件夹中匹配图片并按指定格式保存
    
    参数:
        raw_folder: 包含原始.bmp图像的文件夹
        pse_folder: 包含_pseudo.png或.png图像的文件夹
        output_folder: 保存输出图像的文件夹
        target_folder: 保存目标图像的文件夹
        class_name: 类别名称，用于生成新的文件名
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(target_folder, exist_ok=True)
    
    # 获取raw文件夹中的所有.bmp文件
    bmp_files = [f for f in os.listdir(raw_folder) if f.lower().endswith('.bmp')]
    
    if not bmp_files:
        print(f"警告: 在 {raw_folder} 中没有找到.bmp文件")
        return 0
    
    # 获取pse文件夹中的所有文件用于查找
    pse_files = set(os.listdir(pse_folder))
    
    # 跟踪已处理的索引
    index = 0
    matches = 0
    no_matches = 0
    
    for bmp_file in tqdm(sorted(bmp_files), desc=f"处理 {class_name} 类别"):
        # 提取文件名（不带扩展名）
        name = os.path.splitext(bmp_file)[0]
        
        # 尝试找到对应的伪标签文件
        pseudo_file = f"{name}_pseudo.png"
        regular_file = f"{name}.png"
        
        if pseudo_file in pse_files:
            pse_file = pseudo_file
        elif regular_file in pse_files:
            pse_file = regular_file
        else:
            print(f"警告: 在 {pse_folder} 中没有找到与 {bmp_file} 对应的文件")
            no_matches += 1
            continue
        
        # 设置文件路径
        bmp_path = os.path.join(raw_folder, bmp_file)
        pse_path = os.path.join(pse_folder, pse_file)
        
        # 设置目标文件名
        output_name = f"{class_name}_{index}.png"
        target_name = f"{class_name}_target_{index}.png"
        
        # 设置保存路径
        output_path = os.path.join(output_folder, output_name)
        target_path = os.path.join(target_folder, target_name)
        
        # 复制文件（将bmp转换为png）
        try:
            # 对于原始图像，我们需要读取并保存为png格式
            import cv2
            img = cv2.imread(bmp_path)
            cv2.imwrite(output_path, img)
            
            # 对于伪标签，直接复制
            shutil.copy2(pse_path, target_path)
            
            matches += 1
            index += 1
        except Exception as e:
            print(f"错误: 处理 {bmp_file} 和 {pse_file} 时出错: {str(e)}")
    
    print(f"\n处理完成! 类别 '{class_name}' 共匹配 {matches} 对图像, {no_matches} 对无法匹配")
    return matches

def main():
    parser = argparse.ArgumentParser(description='匹配并重命名图像对')
    parser.add_argument('-r', '--raw', required=True, help='包含原始.bmp图像的文件夹')
    parser.add_argument('-p', '--pse', required=True, help='包含伪标签图像的文件夹')
    parser.add_argument('-o', '--output', required=True, help='保存输出图像的文件夹')
    parser.add_argument('-t', '--target', required=True, help='保存目标图像的文件夹')
    parser.add_argument('-c', '--class_name', required=True, help='类别名称，用于生成文件名')
    
    args = parser.parse_args()
    
    # 验证输入文件夹
    if not os.path.isdir(args.raw):
        print(f"错误: 原始图像文件夹 '{args.raw}' 不存在!")
        return
        
    if not os.path.isdir(args.pse):
        print(f"错误: 伪标签图像文件夹 '{args.pse}' 不存在!")
        return
    
    # 开始处理
    print(f"开始匹配和重命名图像对，类别: {args.class_name}")
    print(f"- 原始图像文件夹: {args.raw}")
    print(f"- 伪标签图像文件夹: {args.pse}")
    print(f"- 输出图像文件夹: {args.output}")
    print(f"- 目标图像文件夹: {args.target}")
    
    total_matches = match_and_save_photos(
        args.raw, 
        args.pse, 
        args.output, 
        args.target,
        args.class_name
    )
    
    print(f"\n总结: 共处理了 {total_matches} 对图像")

if __name__ == "__main__":
    main()