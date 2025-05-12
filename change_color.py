import cv2
import numpy as np
import os

def replace_color_in_images(input_dir, output_dir, new_color=(0, 255, 0)):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # 读取图像
            image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

            # 创建掩膜：任意通道大于10的像素被保留
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            # 检查每个通道是否有值大于10，用逻辑或组合
            mask[(image[:,:,0] > 10) | (image[:,:,1] > 10) | (image[:,:,2] > 10)] = 255

            # 创建一个新图像，背景为黑色
            new_image = np.zeros_like(image)

            # cv2.imshow("mask", mask)
            # cv2.waitKey(0)

            # 将指定颜色填充到掩膜区域
            new_image[mask > 0] = new_color

            # 保存新图像
            cv2.imwrite(output_path, new_image)
            print(f"Processed: {filename}")

# 示例用法
input_folder = "/media/qinyh/KINGSTON/气泡麻点鱼眼标注/鱼眼/111"         # 替换为你的输入文件夹路径
output_folder = "/media/qinyh/KINGSTON/气泡麻点鱼眼标注/鱼眼/222"         # 替换为你的输入文件夹路径
# input_folder = "/media/qinyh/KINGSTON/yuyan_unchanged"         # 替换为你的输入文件夹路径
# output_folder = "/media/qinyh/KINGSTON/yuyan_changed"       # 替换为你的输出文件夹路径
# input_folder = "/media/qinyh/KINGSTON/111"         # 替换为你的输入文件夹路径
# output_folder = "/media/qinyh/KINGSTON/222"         # 替换为你的输入文件夹路径
# target_color = (127,255,0)            # 替换为你想要的颜色 (B, G, R)
# target_color = (0,255,255)            # 替换为你想要的颜色 (B, G, R)
target_color = (238,130,238)            # 替换为你想要的颜色 (B, G, R)

replace_color_in_images(input_folder, output_folder, new_color=target_color)
