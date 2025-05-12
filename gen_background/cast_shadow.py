import cv2
import numpy as np
import random
import os
import argparse

def simulate_shadows(image_path, output_path, max_shadows=10):
    """
    在灰度图上模拟多个阴影区域。
    
    :param image_path: 输入灰度图片的路径
    :param output_path: 输出图片的保存路径
    :param max_shadows: 最大阴影数量
    :return: 操作是否成功
    """
    # 读取灰度图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return False

    # 获取图片分辨率
    height, width = image.shape

    # 随机生成阴影数量
    num_shadows = random.randint(1, max_shadows)

    # 初始化阴影掩模（初始化为全1，表示不减少亮度）
    shadow_mask = np.ones_like(image, dtype=np.float32)

    for _ in range(num_shadows):
        # 随机生成阴影参数
        shadow_center = (random.randint(0, width), random.randint(0, height))  # 阴影中心
        shadow_intensity = random.uniform(0.75, 0.95)  # 阴影强度 (0.3表示减少70%亮度，0.7表示减少30%亮度)
        shadow_radius = random.uniform(500, 1500)  # 阴影半径

        # 创建单个阴影的掩模
        y, x = np.ogrid[:height, :width]
        distance_from_center = np.sqrt((x - shadow_center[0])**2 + (y - shadow_center[1])**2)
        
        # 阴影强度随距离衰减（中心最暗，边缘较亮）
        # 将距离映射到0-1之间，越近中心值越小
        distance_factor = np.clip(distance_from_center / shadow_radius, 0, 1)
        
        # 计算阴影系数，distance_factor为0时最暗，为1时不变
        single_shadow_mask = shadow_intensity + (1 - shadow_intensity) * distance_factor
        
        # 限制在0-1之间
        single_shadow_mask = np.clip(single_shadow_mask, shadow_intensity, 1.0)
        
        # 累积阴影效果（相乘，因为每个系数都是暗化因子）
        shadow_mask *= single_shadow_mask

    # 将阴影掩模应用到原始图片（相乘实现暗化）
    shadow_image = (image * shadow_mask).astype(np.uint8)

    # 保存处理后的图片
    cv2.imwrite(output_path, shadow_image)
    print(f"模拟阴影效果后的图片已保存到: {output_path}")
    return True

def process_folder(input_folder, output_folder, max_shadows=10):
    """
    处理文件夹中的所有图像，应用阴影模拟，并将结果保存到输出文件夹。
    
    :param input_folder: 输入图像文件夹路径
    :param output_folder: 输出图像文件夹路径
    :param max_shadows: 最大阴影数量
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取输入文件夹中的所有图像文件
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'))]
    
    if not image_files:
        print(f"在文件夹 {input_folder} 中没有找到图像文件")
        return
    
    processed_count = 0
    failed_count = 0
    
    for image_file in image_files:
        input_path = os.path.join(input_folder, image_file)
        
        # 生成输出文件名（在原文件名的扩展名前添加_shadow）
        filename, ext = os.path.splitext(image_file)
        output_filename = f"{filename}_shadow{ext}"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"正在处理: {input_path}")
        
        success = simulate_shadows(input_path, output_path, max_shadows)
        
        if success:
            processed_count += 1
        else:
            failed_count += 1
    
    print(f"\n处理完成! 成功处理: {processed_count} 张图像, 失败: {failed_count} 张图像")

def main():
    parser = argparse.ArgumentParser(description='对图像应用阴影效果模拟')
    parser.add_argument('--input_folder', type=str, default="/media/qinyh/KINGSTON/MetaData/background_data_resized/yuyan", help='输入图像文件夹路径')
    # parser.add_argument('--output_folder', type=str, default="/media/qinyh/KINGSTON/GenData/yuyan/yuyan_shadow", help='输出图像文件夹路径')
    parser.add_argument('--max_shadows', type=int, default=10, help='最大阴影数量')
    
    args = parser.parse_args()
    args.output_folder = args.input_folder
    
    process_folder(args.input_folder, args.output_folder, args.max_shadows)

if __name__ == "__main__":
    main()