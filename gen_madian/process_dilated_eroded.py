import os
import cv2
import numpy as np
import argparse

def process_target_image(image_path, kernel_size=5, iterations=2):
    """
    处理目标图像，提取橙色部分，进行腐蚀和膨胀操作
    
    Args:
        image_path: 输入图像路径
        kernel_size: 形态学操作的核大小
        iterations: 腐蚀和膨胀的迭代次数
    
    Returns:
        处理后的图像
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 创建掩膜：任意通道大于10的像素被保留
    orange_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    # 检查每个通道是否有值大于10，用逻辑或组合
    orange_mask[(image[:,:,0] > 10) | (image[:,:,1] > 10) | (image[:,:,2] > 10)] = 255

    # cv2.imshow("Orange Mask", orange_mask)
    # cv2.waitKey(0)
    
    # 创建结构元素用于形态学操作
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # 然后进行膨胀操作
    dilated = cv2.dilate(orange_mask, kernel, iterations=iterations)

    # cv2.imshow("Orange Mask", eroded)
    # cv2.waitKey(0)
    
    # 先进行腐蚀操作
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # cv2.imshow("Orange Mask", dilated)
    # cv2.waitKey(0)
    
    # 创建一个黑色背景
    result = np.zeros_like(image)
    
    # 在掩模区域填充橙色
    orange_color = [0, 165, 255]  # BGR格式下的橙色
    result[eroded > 0] = orange_color
    
    return result

def process_folder(input_folder, kernel_size=5, iterations=2):
    """
    处理文件夹中所有以target.png结尾的图像
    
    Args:
        input_folder: 输入文件夹路径
        kernel_size: 形态学操作的核大小
        iterations: 腐蚀和膨胀的迭代次数
    """
    # 获取所有以target.png结尾的文件
    target_files = [f for f in os.listdir(input_folder) if f.endswith('target.png')]
    
    if not target_files:
        print(f"在文件夹 {input_folder} 中没有找到target.png文件")
        return
    
    processed_count = 0
    failed_count = 0
    
    for file in target_files:
        input_path = os.path.join(input_folder, file)
        
        # 生成输出文件名
        base_name = file.replace('target.png', '')
        output_filename = f"{base_name}target_process.png"
        output_path = os.path.join(input_folder, output_filename)
        
        print(f"处理文件: {input_path}")
        
        # 处理图像
        processed_image = process_target_image(input_path, kernel_size, iterations)
        
        if processed_image is not None:
            # 保存处理后的图像
            cv2.imwrite(output_path, processed_image)
            print(f"保存处理后的图像: {output_path}")
            processed_count += 1
        else:
            failed_count += 1
    
    print(f"\n处理完成! 成功处理: {processed_count} 张图像, 失败: {failed_count} 张图像")

def main():
    parser = argparse.ArgumentParser(description='处理target.png图像，提取橙色部分并进行形态学操作')
    parser.add_argument('--input_folder', type=str, default="/media/qinyh/KINGSTON/MetaData/madian_data", help='输入图像文件夹路径')
    parser.add_argument('--kernel_size', type=int, default=5, help='形态学操作的核大小')
    parser.add_argument('--iterations', type=int, default=2, help='腐蚀和膨胀的迭代次数')
    
    args = parser.parse_args()
    
    process_folder(args.input_folder, args.kernel_size, args.iterations)

if __name__ == "__main__":
    main()