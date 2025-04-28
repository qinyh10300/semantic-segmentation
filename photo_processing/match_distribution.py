import os
import cv2
import numpy as np
from scipy.stats import norm

def get_edge_pixels(image):
    """提取图像的边缘像素值"""
    edges = cv2.Canny(image, 100, 200)  # 使用Canny边缘检测
    edge_pixels = image[edges > 0]  # 提取边缘像素值
    return edge_pixels

def match_distribution(source_pixels, target_mean, target_std):
    """将源像素值调整为目标高斯分布"""
    source_mean = np.mean(source_pixels)
    source_std = np.std(source_pixels)
    # 标准化源像素值
    normalized_pixels = (source_pixels - source_mean) / source_std
    # 调整到目标分布
    matched_pixels = normalized_pixels * target_std + target_mean
    return np.clip(matched_pixels, 0, 255).astype(np.uint8)

def calculate_average_distribution(input_folder):
    """计算所有图像边缘像素的高斯分布参数的平均值"""
    means = []
    stds = []
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            filepath = os.path.join(input_folder, filename)
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            edge_pixels = get_edge_pixels(image)
            if len(edge_pixels) > 0:  # 确保有边缘像素
                means.append(np.mean(edge_pixels))
                stds.append(np.std(edge_pixels))
    # 计算均值和标准差的平均值
    avg_mean = np.mean(means) if means else 0
    avg_std = np.mean(stds) if stds else 1  # 避免标准差为0
    return avg_mean, avg_std

def process_images(input_folder, output_folder):
    """处理文件夹中的所有图片"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 计算目标高斯分布参数
    target_mean, target_std = calculate_average_distribution(input_folder)
    print(f"目标高斯分布参数: 均值={target_mean}, 标准差={target_std}")

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            filepath = os.path.join(input_folder, filename)
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            
            # 提取边缘像素值
            edge_pixels = get_edge_pixels(image)
            
            # 调整边缘像素值分布
            adjusted_edge_pixels = match_distribution(edge_pixels, target_mean, target_std)
            
            # 替换原图中的边缘像素值
            edges = cv2.Canny(image, 100, 200)
            adjusted_image = image.copy()
            adjusted_image[edges > 0] = adjusted_edge_pixels
            
            # 保存处理后的图片
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, adjusted_image)

# 主程序
input_folder = "photo_processing/qipao"  # 替换为你的输入文件夹路径
output_folder = "photo_processing/qipao3"  # 替换为你的输出文件夹路径

process_images(input_folder, output_folder)