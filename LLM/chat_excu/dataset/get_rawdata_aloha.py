import os
import h5py
import numpy as np
from PIL import Image
import csv
import io

def extract_hdf5_data(input_dir, output_base_dir):
    # 获取目录中的所有 .hdf5 文件
    hdf5_files = [f for f in os.listdir(input_dir) if f.endswith('.hdf5')]

    for hdf5_file in hdf5_files:
        input_path = os.path.join(input_dir, hdf5_file)
        output_dir = os.path.join(output_base_dir, os.path.splitext(hdf5_file)[0])
        os.makedirs(output_dir, exist_ok=True)

        print(f"Processing file: {input_path}")
        with h5py.File(input_path, 'r') as h5_file:
            for key in h5_file.keys():
                save_data(h5_file, key, output_dir)

def save_data(h5_file, key, output_dir, base_path=""):
    """
    递归遍历 HDF5 文件中的组和数据集：
      - 如果是 Group，则继续往下
      - 如果是 Dataset，则根据路径判断是否是图片 / action / 其它数据
    """
    full_path = f"{base_path}/{key}".lstrip("/")
    node = h5_file[key]

    if isinstance(node, h5py.Group):
        # 递归遍历子项
        for sub_key in node.keys():
            save_data(node, sub_key, output_dir, full_path)
    elif isinstance(node, h5py.Dataset):
        dataset = node[:]
        if "images" in full_path.lower():
            # 此处 dataset 很可能是压缩后的图像数据，形状类似 (300, 21514)
            save_images(dataset, full_path, output_dir)
        elif "action" in full_path.lower():
            # 保存动作到 CSV
            save_action_csv(dataset, full_path, output_dir)
        else:
            # 其它数据，统一存成 npy
            output_path = os.path.join(output_dir, full_path.replace("/", "_") + ".npy")
            np.save(output_path, dataset)
            print(f"Saved: {output_path}")

def save_images(dataset, full_path, output_dir):
    """
    处理压缩图像数据集。每一步都是一串字节流，需要用 PIL 通过 BytesIO 解码。
    """
    view_name = full_path.split("/")[-1]   # 用最后的字段名当作子目录名 (cam_high, cam_left_wrist, etc.)
    image_dir = os.path.join(output_dir, view_name)
    os.makedirs(image_dir, exist_ok=True)

    # 大概率是 (N, compressed_size)，比如 (300, 21514)
    if dataset.ndim == 2:
        num_steps, compressed_size = dataset.shape
        print(f"Found compressed images at '{full_path}', shape={dataset.shape}")
        for step_idx in range(num_steps):
            # dataset[step_idx] 是一维数组，包含 compressed_size 个字节
            # 需要转换为真正的字节流，然后用 PIL 解码
            # 有些情况下 dataset.dtype 可能是 uint8，也可能是 int8，都做成 bytes() 试一下
            compressed_bytes = dataset[step_idx].tobytes()

            try:
                img_pil = Image.open(io.BytesIO(compressed_bytes))
                # 如果想保持原格式（jpg/png），可以用 .save(image_path, format=...) 指定
                image_path = os.path.join(image_dir, f"step_{step_idx}.png")
                img_pil.save(image_path)
            except Exception as e:
                print(f"[WARNING] Failed to decode image at step {step_idx} in {full_path}: {e}")
        print(f"Saved {num_steps} images to {image_dir}")

    else:
        
        print(f"[WARNING] Unexpected image dataset shape for {full_path}: {dataset.shape}")

def save_action_csv(dataset, full_path, output_dir):
    """
    保存 action 数据为 CSV 文件
    """
    output_path = os.path.join(output_dir, "action.csv")
    with open(output_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        if dataset.ndim == 2:  # (N, action_dim)
            # 写入列名
            writer.writerow([f"Joint_{i}" for i in range(dataset.shape[1])])
            writer.writerows(dataset)
        elif dataset.ndim == 1:  # (action_dim,) 或 (N,)
            writer.writerow(["Action"])
            if dataset.dtype.kind in ['i','f']:
                writer.writerows(dataset.reshape(-1,1))
            else:  # 如果是字符串或其它类型
                writer.writerows([[str(x)] for x in dataset])
        else:
            print(f"[WARNING] Unexpected action dataset shape: {dataset.shape} at {full_path}")
    print(f"Saved action CSV: {output_path}")

if __name__ == "__main__":
    input_directory = "/home/wyr/code/octo/aloha/12_01_ziploc_slide_50_compressed"
    output_directory = "/home/wyr/code/octo/aloha/rawdata_2"
    extract_hdf5_data(input_directory, output_directory)
