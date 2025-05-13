import cv2
import numpy as np
import os
import argparse

def apply_gray_mask_with_fill(image_path, output_path, lower_threshold, upper_threshold):
    """
    对灰度图片应用灰色掩模，保留阈值范围内部分，并填充不规则环形内部。
    
    :param image_path: 输入灰度图片的路径
    :param output_path: 输出图片的保存路径
    :param lower_threshold: 灰度下限阈值
    :param upper_threshold: 灰度上限阈值
    """
    # 读取灰度图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return False

    # 应用灰度掩模，保留在下限阈值到上限阈值之间的像素
    print(upper_threshold, lower_threshold)
    masked_image = np.where((image >= upper_threshold) | (image <= lower_threshold), image, 0).astype(np.uint8)

    # 找到轮廓
    contours, _ = cv2.findContours(masked_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个空白图像用于绘制填充后的轮廓
    filled_image = np.zeros_like(image)

    # 填充轮廓内部
    cv2.drawContours(filled_image, contours, -1, (255), thickness=cv2.FILLED)

    # 在填充的区域内保留原始灰度值
    result_image = np.where(filled_image == 255, image, 0)

    # 保存处理后的图片
    cv2.imwrite(output_path, result_image)
    print(f"处理后的图片已保存到: {output_path}")
    return True

def process_folder(input_folder, output_folder, lower_threshold, upper_threshold):
    """
    处理文件夹中的所有图像，应用灰度掩模和填充，并在输出文件夹中保存结果。
    
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param lower_threshold: 灰度下限阈值
    :param upper_threshold: 灰度上限阈值
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
        
        # 生成输出文件名（在原文件名的.png前添加_filter）
        filename, ext = os.path.splitext(image_file)
        # output_filename = f"{filename}_filter{ext}"
        output_filename = f"{filename}{ext}"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"正在处理: {input_path}")
        
        success = apply_gray_mask_with_fill(input_path, output_path, lower_threshold, upper_threshold)
        
        if success:
            processed_count += 1
        else:
            failed_count += 1
    
    print(f"\n处理完成! 成功处理: {processed_count} 张图像, 失败: {failed_count} 张图像")

def main():
    parser = argparse.ArgumentParser(description='对文件夹中的所有图像应用灰度掩模和填充')
    parser.add_argument('--input_folder', type=str, default="/media/qinyh/KINGSTON/GenData/qipao/qipao_random_make", help='输入图像文件夹路径')
    parser.add_argument('--output_folder', type=str, default="/media/qinyh/KINGSTON/GenData/qipao/qipao_filter", help='输出图像文件夹路径')
    parser.add_argument('--lower_threshold', type=int, default=80, help='灰度下限阈值')
    parser.add_argument('--upper_threshold', type=int, default=100, help='灰度上限阈值')
    
    args = parser.parse_args()
    
    process_folder(args.input_folder, args.output_folder, args.lower_threshold, args.upper_threshold)

if __name__ == "__main__":
    main()
