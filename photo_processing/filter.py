import cv2
import numpy as np

def apply_gray_mask(image_path, output_path, threshold):
    """
    对灰度图片应用灰色掩模，阈值以上部分保留原图，阈值以下部分变为全黑。
    
    :param image_path: 输入灰度图片的路径
    :param output_path: 输出图片的保存路径
    :param threshold: 灰度阈值
    """
    # 读取灰度图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return

    # 应用灰度掩模
    masked_image = np.where(image >= threshold, image, 0)

    # 保存处理后的图片
    cv2.imwrite(output_path, masked_image)
    print(f"处理后的图片已保存到: {output_path}")

# 示例使用
input_image_path = "photo_processing/output_with_multiple_patches_smoothed.bmp"  # 替换为输入图片路径
output_image_path = "photo_processing/smoothed.bmp"  # 替换为输出图片路径
gray_threshold = 128  # 设置灰度阈值

apply_gray_mask(input_image_path, output_image_path, gray_threshold)