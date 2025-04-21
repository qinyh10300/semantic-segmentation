import cv2
import os
import random
import numpy as np

def add_random_patch_to_background(background_path, image_folder):
    # 获取文件夹中的所有小图片文件
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]
    
    # 如果背景图文件夹或图片文件夹为空，返回
    if not background_path or not image_files:
        print("No images found in the folders.")
        return

    # 随机选择一张背景图片
    background = cv2.imread(background_path)

    # 随机选择一张小图片
    selected_image = random.choice(image_files)
    img_path = os.path.join(image_folder, selected_image)
    img = cv2.imread(img_path)

    # 检查小图片大小是否为 512x512
    if img.shape[:2] != (512, 512):
        print(f"Skipping image {selected_image} (not 512x512).")
        return

    # 获取背景图片的大小
    bg_height, bg_width, _ = background.shape

    # 计算随机位置，确保小图片不会超出背景图边界
    max_x = bg_width - img.shape[1]
    max_y = bg_height - img.shape[0]
    
    # 随机生成一个合适的位置
    random_x = random.randint(0, max_x)
    random_y = random.randint(0, max_y)

    # 将小图片放置到背景图上
    background[random_y:random_y + img.shape[0], random_x:random_x + img.shape[1]] = img

    # 显示合成后的图像
    cv2.imshow("Random Patch on Background", background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存合成图
    output_path = "output_with_patch.bmp"
    cv2.imwrite(output_path, background)
    print(f"Image saved as {output_path}")

# 使用示例
background_path = 'pure_color_background.bmp'  # 替换为背景图片文件夹路径
image_folder = 'patches'  # 替换为小图片文件夹路径
add_random_patch_to_background(background_path, image_folder)
