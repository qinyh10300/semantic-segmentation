import cv2
import numpy as np

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    # alpha: 对比度， beta: 亮度
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

# 读取图像
image = cv2.imread("photo_processing/output_with_multiple_patches_smoothed.bmp")

# 调整亮度和对比度
brighter_image = adjust_brightness_contrast(image, alpha=1.2, beta=50)
darker_image = adjust_brightness_contrast(image, alpha=0.8, beta=-50)

# 显示结果
cv2.imshow("Original", image)
cv2.imshow("Brighter", brighter_image)
cv2.imshow("Darker", darker_image)
cv2.waitKey(0)
cv2.destroyAllWindows()