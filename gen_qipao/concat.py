import os
import shutil
import argparse
from pathlib import Path
from tqdm import tqdm

def copy_images(source_folders, destination_folder, image_extensions=None, verbose=True):
    """
    将多个源文件夹中的图片文件复制到目标文件夹
    
    参数:
        source_folders: 源文件夹列表
        destination_folder: 目标文件夹
        image_extensions: 要复制的图片扩展名列表，默认为常见图片格式
        verbose: 是否显示详细信息
    """
    # 如果未指定扩展名，使用默认的图片扩展名
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif', '.webp']
    
    # 确保目标文件夹存在
    os.makedirs(destination_folder, exist_ok=True)
    
    total_copied = 0
    total_skipped = 0
    
    # 处理每个源文件夹
    for source_folder in source_folders:
        if not os.path.exists(source_folder):
            print(f"错误: 源文件夹 '{source_folder}' 不存在")
            continue
            
        # 获取源文件夹中的所有文件
        all_files = []
        for ext in image_extensions:
            all_files.extend(list(Path(source_folder).rglob(f"*{ext}")))
            all_files.extend(list(Path(source_folder).rglob(f"*{ext.upper()}")))
        
        if verbose:
            print(f"在 '{source_folder}' 中找到 {len(all_files)} 个图片文件")
        
        # 复制文件
        for file_path in tqdm(all_files, desc=f"从 {source_folder} 复制文件", disable=not verbose):
            try:
                # 构建目标路径
                rel_path = file_path.relative_to(source_folder)
                dest_path = os.path.join(destination_folder, rel_path.name)
                
                # 检查是否有重名文件
                if os.path.exists(dest_path):
                    # 重命名文件以避免冲突
                    base_name = os.path.splitext(rel_path.name)[0]
                    ext = os.path.splitext(rel_path.name)[1]
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(destination_folder, f"{base_name}_{counter}{ext}")
                        counter += 1
                
                # 复制文件
                shutil.copy2(file_path, dest_path)
                total_copied += 1
                
            except Exception as e:
                print(f"复制 '{file_path}' 时出错: {str(e)}")
                total_skipped += 1
    
    if verbose:
        print(f"\n复制完成: 成功复制 {total_copied} 个文件, 跳过 {total_skipped} 个文件")
        print(f"所有文件已复制到: {destination_folder}")

def main():
    parser = argparse.ArgumentParser(description='将多个文件夹中的图片复制到目标文件夹')
    parser.add_argument('-s', '--sources', required=True, nargs='+', help='源文件夹路径列表')
    parser.add_argument('-d', '--destination', required=True, help='目标文件夹路径')
    parser.add_argument('-e', '--extensions', nargs='+', help='要复制的文件扩展名 (默认: 常见图片格式)')
    parser.add_argument('-q', '--quiet', action='store_true', help='不显示详细信息')
    
    args = parser.parse_args()
    
    # 处理扩展名
    extensions = args.extensions
    if extensions:
        # 确保扩展名以点开头
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    copy_images(args.sources, args.destination, extensions, not args.quiet)

if __name__ == "__main__":
    main()