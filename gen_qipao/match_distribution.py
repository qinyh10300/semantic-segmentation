import os
import cv2
import numpy as np
from scipy.stats import norm

def calculate_average_distribution(input_folder):
    """计算所有图像边缘像素的高斯分布参数的平均值"""
    means = []
    stds = []
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png')) and not filename.endswith(('_target.png')):
            filepath = os.path.join(input_folder, filename)
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            edge_pixels = get_edge_pixels(image)
            if len(edge_pixels) > 0:  # 确保有边缘像素
                mean = np.mean(edge_pixels)
                std = np.std(edge_pixels)
                means.append(mean)
                stds.append(std)
                print(f"图片: {filename}, 边缘像素均值: {mean:.2f}, 标准差: {std:.2f}")
    # 计算均值和标准差的平均值
    avg_mean = np.mean(means) if means else 0
    avg_std = np.mean(stds) if stds else 1  # 避免标准差为0
    return avg_mean, avg_std

def get_edge_pixels(image):
    """提取图像上下左右四个边缘的像素值"""
    height, width = image.shape
    # 上边缘和下边缘
    top_edge = image[0, :]
    bottom_edge = image[-1, :]
    # 左边缘和右边缘
    left_edge = image[:, 0]
    right_edge = image[:, -1]
    # 合并所有边缘像素
    edge_pixels = np.concatenate([top_edge, bottom_edge, left_edge, right_edge])
    return edge_pixels

def match_distribution(image, edge_pixels, target_mean, target_std):
    """将整张图片调整为目标高斯分布，但使边缘像素保持目标分布"""
    source_mean = np.mean(edge_pixels)
    source_std = np.std(edge_pixels)
    if source_std == 0:  # 避免除以0
        return image

    # 标准化整张图片
    normalized_image = (image - source_mean) / source_std
    # 调整到目标分布
    matched_image = normalized_image * target_std + target_mean
    return np.clip(matched_image, 0, 255).astype(np.uint8)

def process_images(input_folder, output_folder):
    """处理文件夹中的所有图片"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 计算目标高斯分布参数
    target_mean, target_std = calculate_average_distribution(input_folder)
    print(f"目标高斯分布参数: 均值={target_mean}, 标准差={target_std}")

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png')) and not filename.endswith(('_target.png')):
            filepath = os.path.join(input_folder, filename)
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            
            # 提取边缘像素值
            edge_pixels = get_edge_pixels(image)
            
            # 调整整张图片，使边缘像素保持目标分布
            adjusted_image = match_distribution(image, edge_pixels, target_mean, target_std)
            
            # 保存处理后的图片
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, adjusted_image)

# 主程序
input_folder = "/media/qinyh/KINGSTON/data/qipao_data"  # 替换为你的输入文件夹路径
output_folder = "/media/qinyh/KINGSTON/data/qipao_data_2"  # 替换为你的输出文件夹路径

process_images(input_folder, output_folder)