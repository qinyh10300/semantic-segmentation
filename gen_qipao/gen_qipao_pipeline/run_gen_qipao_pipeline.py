"""
Main script for UMI SLAM pipeline.
python sample_generation/run_gen_qipao_pipeline.py --meta_data /home/qinyh/codebase/meta_data/qipao -o /home/qinyh/codebase/meta_data/qipao
"""

import sys
import os

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
os.chdir(ROOT_DIR)

# %%
import pathlib
import click
import subprocess

# %%
@click.command()
@click.option('--meta_data', type=str, required=True, help='Meta data file path')
@click.option('-o', '--ouput_dir', type=str, required=True, help='Gen output data file path')
def main(meta_data, ouput_dir):
    print("############## 01_random_make #############")
    script_path = script_dir.joinpath("01_random_make.py")
    print(str(script_path))
    assert script_path.is_file()
    print(str(meta_data))
    cmd = [
        'python', str(script_path),
        '--background', str(meta_data),
        '--img_folder', str(meta_data),
        '--output_dir', str(ouput_dir),
    ]
    result = subprocess.run(cmd)
    assert result.returncode == 0

## %%
if __name__ == "__main__":
    main()