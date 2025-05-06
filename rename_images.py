import os
import shutil

def rename_and_pair_images(source_folder, target_folder):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 获取源文件夹中所有文件
    images = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png'))]

    # 按文件名排序，确保配对一致
    images.sort()

    # 遍历图片并重命名
    index = 1
    for image_name in images:
        if image_name.endswith('_pseudo.png'):
            base_name = image_name.replace('_pseudo.png', '')
            paired_image = f"{base_name}.png"
            if paired_image in images:
                # 重命名原图
                source_path_original = os.path.join(source_folder, paired_image)
                target_path_original = os.path.join(target_folder, f"qipao_{index}.png")
                shutil.copy(source_path_original, target_path_original)

                # 重命名伪标签图
                source_path_pseudo = os.path.join(source_folder, image_name)
                target_path_pseudo = os.path.join(target_folder, f"qipao_{index}_target.png")
                shutil.copy(source_path_pseudo, target_path_pseudo)

                print(f"Renamed and moved: {source_path_original} -> {target_path_original}")
                print(f"Renamed and moved: {source_path_pseudo} -> {target_path_pseudo}")

                index += 1

# 示例用法
source_folder = "sample_generation/raw_data_qipao"
target_folder = "sample_generation/qipao_data"
rename_and_pair_images(source_folder, target_folder)
