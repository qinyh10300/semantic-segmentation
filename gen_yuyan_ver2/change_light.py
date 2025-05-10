import cv2
import numpy as np
import random
import os
import argparse

def simulate_lighting(image_path, output_path, max_lights=10):
    """
    在灰度图上模拟多个光源的光线变化。
    
    :param image_path: 输入灰度图片的路径
    :param output_path: 输出图片的保存路径
    :param max_lights: 最大光源数量
    :return: 操作是否成功
    """
    # 读取灰度图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return False

    # 获取图片分辨率
    height, width = image.shape

    # 随机生成光源数量
    num_lights = random.randint(1, max_lights)

    # 初始化光照掩模
    light_mask = np.zeros_like(image, dtype=np.float32)

    for _ in range(num_lights):
        # 随机生成光源参数
        light_center = (random.randint(0, width), random.randint(0, height))  # 光源中心
        light_intensity = random.uniform(10, 20)  # 光源强度
        light_radius = random.uniform(500, 1500)  # 光源半径

        # 创建单个光源的光照掩模
        y, x = np.ogrid[:height, :width]
        distance_from_center = np.sqrt((x - light_center[0])**2 + (y - light_center[1])**2)
        single_light_mask = np.clip(light_intensity * (1 - distance_from_center / light_radius), 0, light_intensity)

        # 累加光源效果
        light_mask += single_light_mask

    # 将光照掩模叠加到原始图片
    lighted_image = cv2.add(image, light_mask.astype(np.uint8))

    # 保存处理后的图片
    cv2.imwrite(output_path, lighted_image)
    print(f"模拟光线变化后的图片已保存到: {output_path}")
    return True

def process_folder(input_folder, output_folder, max_lights=10):
    """
    处理文件夹中的所有图像，应用光照模拟，并将结果保存到输出文件夹。
    
    :param input_folder: 输入图像文件夹路径
    :param output_folder: 输出图像文件夹路径
    :param max_lights: 最大光源数量
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
        
        # 生成输出文件名（在原文件名的扩展名前添加_light）
        filename, ext = os.path.splitext(image_file)
        output_filename = f"{filename}_light{ext}"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"正在处理: {input_path}")
        
        success = simulate_lighting(input_path, output_path, max_lights)
        
        if success:
            processed_count += 1
        else:
            failed_count += 1
    
    print(f"\n处理完成! 成功处理: {processed_count} 张图像, 失败: {failed_count} 张图像")

def main():
    parser = argparse.ArgumentParser(description='对图像应用光照效果模拟')
    parser.add_argument('--input_folder', type=str, default="/home/qinyh/Downloads/yuyan_output2", help='输入图像文件夹路径')
    parser.add_argument('--output_folder', type=str, default="/home/qinyh/Downloads/yuyan_light2", help='输出图像文件夹路径')
    parser.add_argument('--max_lights', type=int, default=10, help='最大光源数量')
    
    args = parser.parse_args()
    
    process_folder(args.input_folder, args.output_folder, args.max_lights)

if __name__ == "__main__":
    main()