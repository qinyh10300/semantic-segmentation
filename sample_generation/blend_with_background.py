import cv2
import numpy as np

def blend_with_background(filtered_image_path, background_image_path, output_path):
    """
    将过滤后的图片与背景图片进行拼接，纯黑色部分使用背景图填充。
    
    :param filtered_image_path: 过滤后的图片路径
    :param background_image_path: 背景图片路径
    :param output_path: 拼接后的图片保存路径
    """
    # 读取过滤后的图片
    filtered_image = cv2.imread(filtered_image_path, cv2.IMREAD_GRAYSCALE)
    if filtered_image is None:
        print(f"无法读取过滤后的图片: {filtered_image_path}")
        return

    # 读取背景图片
    background_image = cv2.imread(background_image_path, cv2.IMREAD_GRAYSCALE)
    if background_image is None:
        print(f"无法读取背景图片: {background_image_path}")
        return

    # 调整背景图片大小与过滤后的图片一致
    background_image = cv2.resize(background_image, (filtered_image.shape[1], filtered_image.shape[0]))

    # 将过滤图片的纯黑色部分（像素值为0）替换为背景图片的对应像素值
    blended_image = np.where(filtered_image == 0, background_image, filtered_image)

    # 保存拼接后的图片
    cv2.imwrite(output_path, blended_image)
    print(f"拼接后的图片已保存到: {output_path}")

# 示例使用
filtered_image_path = "sample_generation/smoothed_filled.bmp"  # 替换为过滤后的图片路径
background_image_path = "sample_generation/real_background.bmp"  # 替换为背景图片路径
output_image_path = "sample_generation/blended_image.bmp"  # 替换为拼接后的图片保存路径

blend_with_background(filtered_image_path, background_image_path, output_image_path)