import cv2
import numpy as np
import argparse
import os
from math import ceil

def create_large_image_from_tile(input_image_path, output_image_path, target_width=5472, target_height=3648):
    """
    读取一张图片，获取其分辨率，然后通过拼接方法创建一张指定大小的图像
    
    Args:
        input_image_path: 输入图像路径
        output_image_path: 输出图像路径
        target_width: 目标宽度 (默认 5472)
        target_height: 目标高度 (默认 3648)
    
    Returns:
        bool: 操作是否成功
    """
    # 读取输入图像
    tile = cv2.imread(input_image_path)
    
    # 检查图像是否成功读取
    if tile is None:
        print(f"错误：无法读取图像 {input_image_path}")
        return False
    
    # 获取图像分辨率
    tile_height, tile_width, channels = tile.shape
    print(f"输入图像分辨率: {tile_width} x {tile_height}")
    
    # 创建目标大小的空白图像
    large_image = np.zeros((target_height, target_width, channels), dtype=np.uint8)
    
    # 计算需要多少个瓦片来填充大图像
    tiles_x = ceil(target_width / tile_width)
    tiles_y = ceil(target_height / tile_height)
    
    print(f"需要拼接 {tiles_x} x {tiles_y} 个瓦片")
    
    # 通过重复拼贴填充大图像
    for y in range(tiles_y):
        for x in range(tiles_x):
            # 计算当前瓦片应放置的位置
            pos_x = x * tile_width
            pos_y = y * tile_height
            
            # 计算实际可用的瓦片大小（处理边缘情况）
            actual_width = min(tile_width, target_width - pos_x)
            actual_height = min(tile_height, target_height - pos_y)
            
            # 只有当有足够空间时才放置瓦片
            if actual_width > 0 and actual_height > 0:
                large_image[pos_y:pos_y+actual_height, pos_x:pos_x+actual_width] = tile[:actual_height, :actual_width]
    
    # 保存结果
    cv2.imwrite(output_image_path, large_image)
    print(f"已创建大图像: {output_image_path}")
    print(f"输出图像分辨率: {target_width} x {target_height}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='将一张图像拼接成更大的图像')
    parser.add_argument('--input', type=str, default="sample_generation_yuyan/meta1.png", help='输入图像文件路径')
    parser.add_argument('--output', type=str, default="sample_generation_yuyan/meta1_larger.png", help='输出图像文件路径')
    parser.add_argument('--width', type=int, default=5472, help='目标宽度')
    parser.add_argument('--height', type=int, default=3648, help='目标高度')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    create_large_image_from_tile(args.input, args.output, args.width, args.height)

if __name__ == "__main__":
    main()