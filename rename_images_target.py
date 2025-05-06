import os
import shutil

def rename_and_move_images(source_folder, target_folder):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 获取源文件夹中所有以 .bmp 和 .png 结尾的文件
    images = [f for f in os.listdir(source_folder) if f.lower().endswith(('.bmp', '.png'))]

    # 遍历图片并重命名
    for index, image_name in enumerate(images, start=1):
        # 构造新的文件名
        base_name = os.path.splitext(image_name)[0]
        new_name = f"{base_name}.png"
        # 构造源文件和目标文件路径
        source_path = os.path.join(source_folder, image_name)
        target_path = os.path.join(target_folder, new_name)
        # 复制并重命名文件
        shutil.copy(source_path, target_path)
        print(f"Renamed and moved: {source_path} -> {target_path}")

def rename_and_move_pseudo_images(source_folder, target_folder):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 获取源文件夹中所有以 _pseudo.png 结尾的文件
    images = [f for f in os.listdir(source_folder) if f.lower().endswith('_pseudo.png')]

    # 遍历图片并重命名
    for index, image_name in enumerate(images, start=1):
        # 构造新的文件名
        new_name = f"{image_name}"
        # 构造源文件和目标文件路径
        source_path = os.path.join(source_folder, image_name)
        target_path = os.path.join(target_folder, new_name)
        # 复制并重命名文件
        shutil.copy(source_path, target_path)
        print(f"Renamed and moved: {source_path} -> {target_path}")

# 示例用法
source_folder = "sample_generation/qipao"
target_folder = "sample_generation/raw_data_qipao"
rename_and_move_images(source_folder, target_folder)

pseudo_source_folder = "sample_generation/qipao/label"
pseudo_target_folder = "sample_generation/raw_data_qipao"
rename_and_move_pseudo_images(pseudo_source_folder, pseudo_target_folder)
