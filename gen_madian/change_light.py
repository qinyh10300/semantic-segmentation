import cv2
import numpy as np
import random

def simulate_lighting(image_path, output_path, max_lights=10):
    """
    在灰度图上模拟多个光源的光线变化。
    
    :param image_path: 输入灰度图片的路径
    :param output_path: 输出图片的保存路径
    :param max_lights: 最大光源数量
    """
    # 读取灰度图片
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return

    # 获取图片分辨率
    height, width = image.shape

    # 随机生成光源数量
    num_lights = random.randint(1, max_lights)

    # 初始化光照掩模
    light_mask = np.zeros_like(image, dtype=np.float32)

    for _ in range(num_lights):
        # 随机生成光源参数
        light_center = (random.randint(0, width), random.randint(0, height))  # 光源中心
        print(f"光源位置: {light_center}")
        light_intensity = random.uniform(10, 30)  # 光源强度
        light_radius = random.uniform(500, 1500)  # 光源半径

        # 创建单个光源的光照掩模
        y, x = np.ogrid[:height, :width]
        distance_from_center = np.sqrt((x - light_center[0])**2 + (y - light_center[1])**2)
        single_light_mask = np.clip(light_intensity * (1 - distance_from_center / light_radius), 0, light_intensity)

        # 累加光源效果
        light_mask += single_light_mask

    # 将光照掩模叠加到原始图片
    lighted_image = cv2.add(image, light_mask.astype(np.uint8))

    # 保存处理后的图片
    cv2.imwrite(output_path, lighted_image)
    print(f"模拟光线变化后的图片已保存到: {output_path}")

# 示例使用
input_image_path = "gen_madian/back.bmp"  # 替换为输入图片路径
output_image_path = "gen_madian/output/back_lighted.bmp"  # 替换为输出图片路径

simulate_lighting(input_image_path, output_image_path)