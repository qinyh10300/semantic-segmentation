import cv2
import numpy as np

def apply_gray_mask_with_fill(image_path, output_path, threshold, erosion_iterations=1, dilation_iterations=1):
    """
    对灰度图片应用灰色掩模，保留阈值以上部分，并填充不规则环形内部。
    同时加入腐蚀和膨胀操作以优化结果。
    
    :param image_path: 输入灰度图片的路径
    :param output_path: 输出图片的保存路径
    :param threshold: 灰度阈值
    :param erosion_iterations: 腐蚀操作的迭代次数
    :param dilation_iterations: 膨胀操作的迭代次数
    """
    # 读取灰度图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return

    # 应用灰度掩模
    masked_image = np.where(image <= threshold, image, 0).astype(np.uint8)

    # 找到轮廓
    contours, _ = cv2.findContours(masked_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个空白图像用于绘制填充后的轮廓
    filled_image = np.zeros_like(image)

    # 填充轮廓内部
    cv2.drawContours(filled_image, contours, -1, (255), thickness=cv2.FILLED)

    # 腐蚀操作
    kernel = np.ones((15, 15), np.uint8)  # 定义一个 3x3 的核
    eroded_image = cv2.erode(filled_image, kernel, iterations=erosion_iterations)

    # 膨胀操作
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=dilation_iterations)

    # 在填充的区域内保留原始灰度值
    result_image = np.where(dilated_image == 255, image, 0)

    # 保存处理后的图片
    cv2.imwrite(output_path, result_image)
    print(f"处理后的图片已保存到: {output_path}")

# 示例使用
input_image_path = "sample_generation_yuyan/output_with_multiple_patches_smoothed.bmp"  # 替换为输入图片路径
output_image_path = "sample_generation_yuyan/smoothed_filled_with_morphology.bmp"  # 替换为输出图片路径
gray_threshold = 80  # 设置灰度阈值

# 调用函数时指定腐蚀和膨胀的迭代次数
apply_gray_mask_with_fill(input_image_path, output_image_path, gray_threshold, erosion_iterations=2, dilation_iterations=2)