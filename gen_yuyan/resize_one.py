import cv2
import argparse
import os
from pathlib import Path

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
            print(f"已将图像缩放至 {target_width}x{target_height} 并保存到 '{output_path}'")
            return True
        else:
            print(f"错误: 无法保存图像到 '{output_path}'")
            return False
    
    except Exception as e:
        print(f"处理图像时出错: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='将图像缩放到指定分辨率')
    parser.add_argument('-i', '--input', default="gen_yuyan2/Background/back_meta.png", help='输入图像路径')
    parser.add_argument('-o', '--output', help='输出图像路径 (默认在原图文件名后添加 _resized)')
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
    
    # 处理输出路径
    if not args.output:
        input_path = Path(args.input)
        output_path = input_path.parent / f"{input_path.stem}_resized{input_path.suffix}"
        args.output = str(output_path)
    
    # 缩放图像
    success = resize_image(args.input, args.output, args.width, args.height, interpolation)
    if success:
        print("图像处理完成")
    else:
        print("图像处理失败")

if __name__ == "__main__":
    main()