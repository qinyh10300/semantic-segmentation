import os
import argparse
from PIL import Image
import glob

def convert_images_to_png(input_folder, output_folder=None, delete_originals=False):
    """
    将文件夹中所有图像文件转换为PNG格式
    
    Args:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径，如果不指定则在原路径保存
        delete_originals: 是否删除原始文件
    """
    # 如果指定了输出文件夹，确保它存在
    if output_folder and output_folder != input_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = ['*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tiff', '*.tif', '*.webp']
    
    # 计数器
    converted_count = 0
    skipped_count = 0
    
    # 遍历所有支持的图像格式
    for extension in image_extensions:
        # 获取匹配的文件
        file_pattern = os.path.join(input_folder, extension)
        image_files = glob.glob(file_pattern)
        
        for image_path in image_files:
            try:
                # 获取文件名（不带扩展名）
                filename = os.path.basename(image_path)
                name, _ = os.path.splitext(filename)
                
                # 确定目标路径
                target_folder = output_folder if output_folder else input_folder
                png_path = os.path.join(target_folder, f"{name}.png")
                
                # 如果文件已经是 PNG 且保存在同一位置，则跳过
                if image_path.lower().endswith('.png') and os.path.dirname(image_path) == target_folder:
                    print(f"跳过: {image_path} (已经是PNG格式)")
                    skipped_count += 1
                    continue
                
                # 打开并转换图像
                with Image.open(image_path) as img:
                    # 保存为PNG
                    img.save(png_path, 'PNG')
                    converted_count += 1
                    print(f"转换: {image_path} -> {png_path}")
                
                # 如果需要删除原始文件，且不是PNG，或者保存到了不同的位置
                if delete_originals and (not image_path.lower().endswith('.png') or input_folder != target_folder):
                    os.remove(image_path)
                    print(f"删除原文件: {image_path}")
                
            except Exception as e:
                print(f"处理文件 {image_path} 时出错: {str(e)}")
                skipped_count += 1
    
    print(f"\n转换完成! 成功转换: {converted_count} 个文件, 跳过: {skipped_count} 个文件")

def main():
    parser = argparse.ArgumentParser(description='将文件夹中所有图像转换为PNG格式')
    parser.add_argument('--input_folder', type=str, default="/home/qinyh/Downloads/yuyan_raw", help='输入图像文件夹路径')
    parser.add_argument('--output_folder', type=str, default="/home/qinyh/Downloads/yuyan_pro", help='输出图像文件夹路径（可选，默认使用输入文件夹）')
    parser.add_argument('--delete_originals', action='store_true', help='转换后删除原始文件')
    
    args = parser.parse_args()
    
    convert_images_to_png(args.input_folder, args.output_folder, args.delete_originals)

if __name__ == "__main__":
    main()