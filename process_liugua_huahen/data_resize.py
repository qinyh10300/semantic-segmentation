import os
from PIL import Image

def resize_images(input_folder, output_folder, target_size_width):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图片文件
    for filename in os.listdir(input_folder):
        # 只处理图片文件，假设图片格式为常见的png、jpg、jpeg等
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'bmp')):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            # 打开图像文件
            with Image.open(input_image_path) as img:
                # 获取原图分辨率
                original_width, original_height = img.size

                # 计算等比例缩放的尺寸
                aspect_ratio = original_width / original_height
                target_width, target_height = target_size_width, int(target_size_width / aspect_ratio)

                # 等比例resize图像
                resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # 保存到输出文件夹
                resized_img.save(output_image_path)
                print(f"Saved resized image: {output_image_path}")

# 示例：将文件夹中的图片等比例resize到1920x1280，并保存在另一个文件夹
# input_folder = r'D:\\大三下\\机器人与智能制造探索\\Segmentation\\data_resize'
# output_folder = r'D:\\大三下\\机器人与智能制造探索\\Segmentation\\data_recover'
input_folder = "/home/qinyh/codebase/UNet-Implement/dataset/liugua/liugua"
output_folder = "/home/qinyh/codebase/UNet-Implement/dataset/liugua/liugua_1"
# original_size = (5472, 3648)
target_size_width = 1920

resize_images(input_folder, output_folder, target_size_width)
