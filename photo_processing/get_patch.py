import cv2
import os

def split_image(image_path, patch_size=(512, 512), output_folder="patches"):
    # 读取图片
    img = cv2.imread(image_path)
    
    # 获取图片的宽和高
    height, width, _ = img.shape
    patch_height, patch_width = patch_size
    
    # 创建保存小 patch 的文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 切割图片
    patch_count = 0
    for y in range(0, height, patch_height):
        for x in range(0, width, patch_width):
            # 计算每个小块的区域
            patch = img[y:y+patch_height, x:x+patch_width]
            
            # 处理图片边界问题（如果小块的大小超过原图大小时）
            if patch.shape[0] != patch_height or patch.shape[1] != patch_width:
                # 填充边缘部分（如果需要）
                patch = cv2.copyMakeBorder(
                    patch, 
                    0, patch_height - patch.shape[0], 
                    0, patch_width - patch.shape[1], 
                    cv2.BORDER_CONSTANT, value=(0, 0, 0)
                )
            
            # 保存切割后的 patch
            patch_filename = f"patch_{patch_count:04d}.bmp"
            patch_path = os.path.join(output_folder, patch_filename)
            cv2.imwrite(patch_path, patch)
            patch_count += 1
    
    print(f"Total patches saved: {patch_count}")

# 使用示例
image_path = 'Image_20250108162518871.bmp'  # 替换为图片的路径
split_image(image_path, patch_size=(512, 512), output_folder="patches")
