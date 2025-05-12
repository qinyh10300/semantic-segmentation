import os
import cv2
import argparse
from pathlib import Path
from tqdm import tqdm

def convert_to_png(input_folder, output_folder=None, delete_original=False):
    """
    将指定文件夹中的所有图片转换为PNG格式
    
    参数:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径，如果不指定则使用原文件夹
        delete_original: 是否删除原始文件
    """
    # 确定输出文件夹
    if output_folder is None:
        output_folder = input_folder
    else:
        os.makedirs(output_folder, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = ['.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.gif', '.webp']
    
    # 获取所有文件
    all_files = []
    for ext in image_extensions:
        all_files.extend(list(Path(input_folder).glob(f'*{ext}')))
        all_files.extend(list(Path(input_folder).glob(f'*{ext.upper()}')))
    
    if not all_files:
        print(f"在 {input_folder} 中未找到需要转换的图片文件")
        return
    
    print(f"找到 {len(all_files)} 个图片文件需要转换")
    
    # 转换每个文件
    success_count = 0
    for file_path in tqdm(all_files, desc="转换进度"):
        try:
            # 读取图像
            img = cv2.imread(str(file_path), cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"无法读取文件: {file_path}")
                continue
            
            # 构建新文件名
            new_filename = file_path.stem + ".png"
            output_path = os.path.join(output_folder, new_filename)
            
            # 保存为PNG
            cv2.imwrite(output_path, img)
            
            # 如果需要，删除原始文件
            if delete_original and str(file_path) != output_path:
                os.remove(file_path)
            
            success_count += 1
        except Exception as e:
            print(f"处理 {file_path} 时出错: {str(e)}")
    
    print(f"成功转换 {success_count}/{len(all_files)} 个文件为PNG格式")

def main():
    parser = argparse.ArgumentParser(description='将文件夹中的图片转换为PNG格式')
    parser.add_argument('-i', '--input', default="/media/qinyh/KINGSTON1/liugua_output_bmp", help='输入文件夹路径')
    parser.add_argument('-o', '--output', default="/media/qinyh/KINGSTON1/liugua_output2", help='输出文件夹路径 (默认与输入相同)')
    parser.add_argument('-d', '--delete', action='store_true', help='转换后删除原始文件')
    
    args = parser.parse_args()
    
    convert_to_png(args.input, args.output, args.delete)

if __name__ == "__main__":
    main()