import os
import shutil
import argparse
from PIL import Image

def process_images(input_folder, output_folder):
    """
    处理input文件夹中的图像文件，保存到output文件夹
    
    Args:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取input文件夹中的所有文件
    all_files = os.listdir(input_folder)
    
    source_images = []
    for file in all_files:
        filename, extension = os.path.splitext(file)
        if extension.lower() in ['.png']:
            if not filename.endswith('_pseudo'):
                source_images.append(file)
    
    # 对文件名进行排序以确保一致的处理顺序
    source_images.sort()
    
    # 处理计数
    processed_count = 0
    skipped_count = 0
    
    # 处理每个源图像
    start_index = 64
    for index, source_file in enumerate(source_images, 1):
        source_path = os.path.join(input_folder, source_file)
        
        # 获取源文件的文件名（不含扩展名）
        filename, extension = os.path.splitext(source_file)
        
        # 构建对应的pseudo文件名
        pseudo_filename = f"{filename}_pseudo{extension}"
        pseudo_path = os.path.join(input_folder, pseudo_filename)
        
        # 检查对应的pseudo文件是否存在
        if pseudo_filename not in all_files:
            # 尝试其他可能的扩展名
            alt_extensions = ['.png'] if extension.lower() in ['.png'] else []
            found = False
            for alt_ext in alt_extensions:
                alt_pseudo_filename = f"{filename}_pseudo{alt_ext}"
                alt_pseudo_path = os.path.join(input_folder, alt_pseudo_filename)
                if alt_pseudo_filename in all_files:
                    pseudo_filename = alt_pseudo_filename
                    pseudo_path = alt_pseudo_path
                    found = True
                    break
            
            if not found:
                print(f"警告: 找不到文件 {source_file} 对应的pseudo文件")
                skipped_count += 1
                continue
        
        # 构建目标文件路径
        target_source_path = os.path.join(output_folder, f"qipao_{start_index+index}.png")
        target_pseudo_path = os.path.join(output_folder, f"qipao_{start_index+index}_target.png")
        
        try:
            # 转换并保存源图像
            img_source = Image.open(source_path)
            img_source.save(target_source_path)
            
            # 转换并保存pseudo图像
            img_pseudo = Image.open(pseudo_path)
            img_pseudo.save(target_pseudo_path)
            
            print(f"处理: {source_file} -> madian_{start_index+index}.png")
            print(f"处理: {pseudo_filename} -> madian_{start_index+index}_target.png")
            
            processed_count += 1
        except Exception as e:
            print(f"处理文件 {source_file} 时出错: {e}")
            skipped_count += 1
    
    print(f"\n处理完成! 成功处理: {processed_count} 对图像, 跳过: {skipped_count} 个文件")

def main():
    parser = argparse.ArgumentParser(description='处理图像文件并重命名')
    parser.add_argument('--input_folder', type=str, default="/media/qinyh/KINGSTON/qipao_change_extension", help='输入图像文件夹路径')
    parser.add_argument('--output_folder', type=str, default="/media/qinyh/KINGSTON/qipao_data", help='输出图像文件夹路径')
    
    args = parser.parse_args()
    
    process_images(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()