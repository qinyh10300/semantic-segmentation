import cv2
import numpy as np
import os
import argparse

def blend_with_background(filtered_image_path, background_image_path, output_path):
    """
    将过滤后的图片与背景图片进行拼接，纯黑色部分使用背景图填充。
    
    :param filtered_image_path: 过滤后的图片路径
    :param background_image_path: 背景图片路径
    :param output_path: 拼接后的图片保存路径
    :return: 操作是否成功
    """
    # 读取过滤后的图片
    filtered_image = cv2.imread(filtered_image_path, cv2.IMREAD_GRAYSCALE)
    if filtered_image is None:
        print(f"无法读取过滤后的图片: {filtered_image_path}")
        return False

    # 读取背景图片
    background_image = cv2.imread(background_image_path, cv2.IMREAD_GRAYSCALE)
    if background_image is None:
        print(f"无法读取背景图片: {background_image_path}")
        return False

    # 调整背景图片大小与过滤后的图片一致
    background_image = cv2.resize(background_image, (filtered_image.shape[1], filtered_image.shape[0]))

    # 将过滤图片的纯黑色部分（像素值为0）替换为背景图片的对应像素值
    blended_image = np.where(filtered_image == 0, background_image, filtered_image)

    # 对生成的图像进行平滑处理（高斯模糊）
    blended_image = cv2.GaussianBlur(blended_image, (7, 7), 0)

    # 保存拼接后的图片
    cv2.imwrite(output_path, blended_image)
    print(f"拼接后的图片已保存到: {output_path}")
    return True

def process_folder(input_folder, background_image_path, output_folder):
    """
    处理文件夹中的所有图像，应用blend_with_background函数，并将结果保存到输出文件夹。
    
    :param input_folder: 输入图像文件夹路径
    :param background_image_path: 背景图像路径
    :param output_folder: 输出图像文件夹路径
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
        
        # 生成输出文件名（在原文件名的扩展名前添加_blend）
        filename, ext = os.path.splitext(image_file)
        output_filename = f"{filename}_blend{ext}"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"正在处理: {input_path}")
        
        success = blend_with_background(input_path, background_image_path, output_path)
        
        if success:
            processed_count += 1
        else:
            failed_count += 1
    
    print(f"\n处理完成! 成功处理: {processed_count} 张图像, 失败: {failed_count} 张图像")

def main():
    parser = argparse.ArgumentParser(description='将过滤后的图片与背景图片进行拼接')
    parser.add_argument('--input_folder', type=str, default="gen_qipao/output/output_filter", help='输入图像文件夹路径')
    parser.add_argument('--background', type=str, default="gen_qipao/Background.bmp", help='背景图像路径')
    parser.add_argument('--output_folder', type=str, default="gen_qipao/output/output_blend", help='输出图像文件夹路径')
    
    args = parser.parse_args()
    
    process_folder(args.input_folder, args.background, args.output_folder)

if __name__ == "__main__":
    main()