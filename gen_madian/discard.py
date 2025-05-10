
import cv2
import os
import random
import numpy as np

def add_multiple_patches_to_background(background_path, img_folder, num_patches=5, output_dir="gen_madian/output"):
    """
    将多个图像补丁添加到背景图像，并根据对应的目标掩码确定哪些像素需要被保留
    
    :param background_path: 背景图像的路径
    :param img_folder: 包含补丁图像的文件夹路径
    :param num_patches: 要添加的补丁数量
    :param output_dir: 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    background = cv2.imread(background_path)

    # 获取背景图片的大小
    bg_height, bg_width, _ = background.shape

    # 获取文件夹中的所有图片路径（不包括target图像）
    img_files = []
    target_files = {}
    
    # 遍历文件夹获取匹配的图像对
    for file in os.listdir(img_folder):
        if file.endswith('.png') and '_target_process.png' not in file:
            # 构建对应的target文件名
            base_name = os.path.splitext(file)[0]
            target_file = f"{base_name}_target_process.png"
            target_path = os.path.join(img_folder, target_file)
            
            # 检查target文件是否存在
            if os.path.exists(target_path):
                img_files.append(os.path.join(img_folder, file))
                target_files[os.path.join(img_folder, file)] = target_path

    if not img_files:
        print(f"文件夹 {img_folder} 中没有找到有效的图像对！")
        return

    # 存储已放置的区域
    placed_regions = []

    def is_overlapping(x, y, width, height):
        """检查新区域是否与已放置的区域重叠"""
        for px, py, pw, ph in placed_regions:
            if not (x + width <= px or px + pw <= x or y + height <= py or py + ph <= y):
                return True
        return False

    for _ in range(num_patches):
        for _ in range(100):  # 尝试最多100次找到一个不重叠的位置
            # 随机选择一张图片
            img_path = random.choice(img_files)
            img = cv2.imread(img_path)

            if img is None:
                print(f"无法读取图片：{img_path}")
                continue
                
            # 读取对应的target掩码图像
            target_path = target_files[img_path]
            target_mask = cv2.imread(target_path)
            # print(target_path, img_path)
            
            if target_mask is None:
                print(f"无法读取对应的target图像：{target_path}")
                continue
                
            # 确保图像和掩码大小相同
            if img.shape != target_mask.shape:
                print(f"图像和掩码大小不一致: {img_path}, {target_path}")
                continue

            img_height, img_width, _ = img.shape

            # 随机生成一个合适的位置
            random_x = random.randint(0, bg_width - img_width)
            random_y = random.randint(0, bg_height - img_height)

            # 检查是否与已放置的区域重叠
            if not is_overlapping(random_x, random_y, img_width, img_height):
                # 获取背景中要放置图像的区域
                bg_patch = background[random_y:random_y + img_height, random_x:random_x + img_width]
                
                # 创建掩码，黑色像素表示不保留的区域
                orange_mask = np.ones_like(target_mask[:,:,0], dtype=bool)
                                
                # 检测黑色区域（所有通道接近0）
                # 像素被认为是黑色的条件：所有通道值都小于阈值（例如30）
                black_threshold = 30
                is_black = np.logical_and(
                    np.logical_and(target_mask[:,:,0] < black_threshold, target_mask[:,:,1] < black_threshold),
                    target_mask[:,:,2] < black_threshold
                )

                # 将黑色区域设为False（不保留），其他区域为True（保留）
                orange_mask = np.logical_not(is_black)
                
                # 创建新的合成图像，只在掩码为True的地方使用原图像，其他地方保留背景
                for i in range(img_height):
                    for j in range(img_width):
                        if orange_mask[i, j]:
                            bg_patch[i, j] = img[i, j]
                
                # 将修改后的区域放回背景
                background[random_y:random_y + img_height, random_x:random_x + img_width] = bg_patch
                placed_regions.append((random_x, random_y, img_width, img_height))
                break
                
    # 保存结果图像
    output_path = os.path.join(output_dir, "output_with_multiple_patches.bmp")
    cv2.imwrite(output_path, background)
    
    # 对生成的图像进行平滑处理（高斯模糊）
    smoothed_background = cv2.GaussianBlur(background, (5, 5), 0)
    
    # 保存平滑处理后的图像
    output_path_smoothed = os.path.join(output_dir, "output_with_multiple_patches_smoothed.bmp")
    cv2.imwrite(output_path_smoothed, smoothed_background)
    
    print(f"图像已保存为 {output_path}")
    print(f"平滑处理后的图像已保存为 {output_path_smoothed}")
    
    return output_path, output_path_smoothed

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='将多个图像补丁添加到背景图像')
    parser.add_argument('--background', type=str, default="gen_madian/output/back_lighted.bmp", help='背景图像路径')
    parser.add_argument('--img_folder', type=str, default="/home/qinyh/Downloads/madian_final", help='包含图像补丁的文件夹路径')
    parser.add_argument('--num_patches', type=int, default=100, help='要添加的补丁数量')
    parser.add_argument('--output_dir', type=str, default="gen_madian/output", help='输出目录')
    
    args = parser.parse_args()
    
    add_multiple_patches_to_background(args.background, args.img_folder, args.num_patches, args.output_dir)

if __name__ == "__main__":
    main()
