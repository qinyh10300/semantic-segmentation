import cv2
import argparse
import os
from pathlib import Path
from tqdm import tqdm

def resize_image(input_path, output_path, target_width, target_height, interpolation=cv2.INTER_LINEAR):
    """
    将图像缩放到指定分辨率
    
    参数:
        input_path: 输入图像路径
        output_path: 输出图像路径
        target_width: 目标宽度
        target_height: 目标高度
        interpolation: 插值方法，默认为线性插值
    
    返回:
        bool: 是否成功
    """
    try:
        # 读取图像
        img = cv2.imread(input_path)
        if img is None:
            print(f"错误: 无法读取图像 '{input_path}'")
            return False
        
        # 缩放图像
        resized_img = cv2.resize(img, (target_width, target_height), interpolation=interpolation)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # 保存图像
        result = cv2.imwrite(output_path, resized_img)
        if result:
            return True
        else:
            print(f"错误: 无法保存图像到 '{output_path}'")
            return False
    
    except Exception as e:
        print(f"处理图像时出错 '{input_path}': {str(e)}")
        return False

def resize_folder(input_folder, output_folder, target_width, target_height, interpolation=cv2.INTER_LINEAR):
    """
    批量处理文件夹中的所有图片
    
    参数:
        input_folder: 输入文件夹
        output_folder: 输出文件夹
        target_width: 目标宽度
        target_height: 目标高度
        interpolation: 插值方法
    """
    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
    
    # 获取所有图片文件
    image_files = []
    for ext in image_extensions:
        image_files.extend(list(Path(input_folder).glob(f'*{ext}')))
        image_files.extend(list(Path(input_folder).glob(f'*{ext.upper()}')))
    
    if not image_files:
        print(f"错误: 在 '{input_folder}' 中未找到图像文件")
        return False
    
    print(f"找到 {len(image_files)} 个图像文件需要处理")
    successful_count = 0
    
    # 使用tqdm显示进度条
    for input_path in tqdm(image_files, desc="缩放处理进度"):
        output_path = os.path.join(output_folder, input_path.name)
        if resize_image(str(input_path), output_path, target_width, target_height, interpolation):
            successful_count += 1
    
    print(f"处理完成: {successful_count}/{len(image_files)} 个文件成功缩放到 {target_width}x{target_height}")
    return successful_count > 0

def main():
    parser = argparse.ArgumentParser(description='将图像缩放到指定分辨率')
    parser.add_argument('-i', '--input', default="/media/qinyh/KINGSTON/MetaData/background_data", help='输入图像路径或文件夹')
    parser.add_argument('-o', '--output', default="/media/qinyh/KINGSTON/MetaData/background_data_resized", help='输出图像路径或文件夹 (单个文件时默认在原文件名后添加 _resized)')
    parser.add_argument('-w', '--width', type=int, default=5472, help='目标宽度')
    parser.add_argument('--height', type=int, default=3648, help='目标高度')
    parser.add_argument('--method', type=str, default='linear', 
                        choices=['nearest', 'linear', 'cubic', 'area', 'lanczos'],
                        help='插值方法 (默认: linear)')
    
    args = parser.parse_args()
    
    # 设置插值方法
    interpolation_methods = {
        'nearest': cv2.INTER_NEAREST,
        'linear': cv2.INTER_LINEAR,
        'cubic': cv2.INTER_CUBIC,
        'area': cv2.INTER_AREA,
        'lanczos': cv2.INTER_LANCZOS4
    }
    
    interpolation = interpolation_methods.get(args.method, cv2.INTER_LINEAR)
    
    # 检查输入是文件还是文件夹
    input_path = Path(args.input)
    if input_path.is_dir():
        # 处理整个文件夹
        if not args.output:
            output_folder = str(input_path) + "_resized"
        else:
            output_folder = args.output
        
        success = resize_folder(
            str(input_path), 
            output_folder, 
            args.width, 
            args.height, 
            interpolation
        )
        
        if success:
            print(f"文件夹处理完成，输出到: {output_folder}")
        else:
            print("文件夹处理失败")
    else:
        # 处理单个文件
        if not args.output:
            output_path = input_path.parent / f"{input_path.stem}_resized{input_path.suffix}"
            args.output = str(output_path)
        
        success = resize_image(args.input, args.output, args.width, args.height, interpolation)
        
        if success:
            print(f"图像处理完成: '{args.output}'")
        else:
            print("图像处理失败")

if __name__ == "__main__":
    main()