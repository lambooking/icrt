import os
import h5py
import numpy as np
from PIL import Image

def extract_h5_datasets(h5_file_path, output_dir):
    """
    从单个h5文件中提取数据集到输出目录下。
    输出规则：
    - 保留原h5文件名为前缀。
    - 'rgb'包含在数据集名称中 -> RGB图像数据，保存PNG
    - 'd'开头的数据集 -> 深度图数据(如(H,W)或(H,W,1))，保存PNG
    - 其他数值数据:
      * 1D或2D数组: CSV
      * 3D及以上数组: NPY
    """
    os.makedirs(output_dir, exist_ok=True)
    original_filename = os.path.splitext(os.path.basename(h6_file_path))[0]

    def save_depth_data(data, dataset_dir, prefix):
        # 对深度数据进行维度检查，如果最后一维是1，则使用squeeze去掉
        # 这样 (H,W,1) -> (H,W)
        if data.ndim == 3 and data.shape[-1] == 1:import os
import h5py
import numpy as np
from PIL import Image

def extract_h5_datasets(h5_file_path, output_dir):
    """
    从单个h5文件中提取数据集到输出目录下。
    输出规则：
    - 保留原h5文件名为前缀。
    - 'rgb'包含在数据集名称中 -> RGB图像数据，保存PNG
    - 'd'开头的数据集 -> 深度图数据(如(H,W)或(H,W,1))，保存PNG
    - 其他数值数据:
      * 1D或2D数组: CSV
      * 3D及以上数组: NPY
    """
    os.makedirs(output_dir, exist_ok=True)
    original_filename = os.path.splitext(os.path.basename(h5_file_path))[0]

    def save_depth_data(data, dataset_dir, prefix):
        # 对深度数据进行维度检查，如果最后一维是1，则使用squeeze去掉
        # 这样 (H,W,1) -> (H,W)
        if data.ndim == 3 and data.shape[-1] == 1:
            data = np.squeeze(data, axis=-1)  # 去掉最后一维

        # 现在的data应是 (H,W) 或 (N,H,W)
        if data.ndim == 3:
            # 多帧深度图 (N, H, W)
            for i in range(data.shape[0]):
                depth_img = data[i].astype(np.uint16)
                img = Image.fromarray(depth_img, mode='I;16')
                img.save(os.path.join(dataset_dir, f"{prefix}_{i}.png"))
        elif data.ndim == 2:
            # 单张深度图 (H, W)
            depth_img = data.astype(np.uint16)
            img = Image.fromarray(depth_img, mode='I;16')
            img.save(os.path.join(dataset_dir, f"{prefix}.png"))
        else:
            # 若维度异常需特殊处理
            raise ValueError(f"Unexpected depth data dimensions: {data.shape}")

    with h5py.File(h5_file_path, 'r') as f:
        
        def visit_func(name, node):
            if isinstance(node, h5py.Dataset):
                data = node[()]
                path_parts = name.split('/')
                dataset_dir = os.path.join(output_dir, *path_parts)
                os.makedirs(dataset_dir, exist_ok=True)

                if 'rgb' in name:
                    # RGB图像数据
                    if data.ndim == 4:
                        # (N, H, W, C)
                        for i, img_arr in enumerate(data):
                            img = Image.fromarray(img_arr.astype(np.uint8))
                            img.save(os.path.join(dataset_dir, f"{original_filename}_{i}.png"))
                    else:
                        # (H, W, C)
                        img = Image.fromarray(data.astype(np.uint8))
                        img.save(os.path.join(dataset_dir, f"{original_filename}.png"))
                elif name.split('/')[0].startswith('d'):
                    # 深度图数据 (H,W) 或 (H,W,1) 或 (N,H,W) 或 (N,H,W,1)
                    save_depth_data(data, dataset_dir, original_filename)
                else:
                    # 数值数据
                    if data.ndim <= 2:
                        # 1D或2D数据, 保存CSV
                        np.savetxt(os.path.join(dataset_dir, f"{original_filename}.csv"), data, delimiter=",")
                    else:
                        # 3D及以上维度的数据，以npy保存
                        np.save(os.path.join(dataset_dir, f"{original_filename}.npy"), data)
        
        f.visititems(visit_func)

def batch_convert_h5(root_dir):
    """
    从root_dir开始递归搜索所有的h5文件，
    对每个h5文件在其所在目录下创建extracted文件夹，将数据输出。
    文件名中保留原来的h5文件名前缀。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                h5_file_path = os.path.join(dirpath, filename)
                output_dir = os.path.join(dirpath, 'extracted')
                print(f"Extracting from {h5_file_path} to {output_dir}")
                extract_h5_datasets(h5_file_path, output_dir)

            data = np.squeeze(data, axis=-1)  # 去掉最后一维

        # 现在的data应是 (H,W) 或 (N,H,W)
        if data.ndim == 3:
            # 多帧深度图 (N, H, W)
            for i in range(data.shape[0]):
                depth_img = data[i].astype(np.uint16)
                img = Image.fromarray(depth_img, mode='I;16')
                img.save(os.path.join(dataset_dir, f"{prefix}_{i}.png"))
        elif data.ndim == 2:
            # 单张深度图 (H, W)
            depth_img = data.astype(np.uint16)
            img = Image.fromarray(depth_img, mode='I;16')
            img.save(os.path.join(dataset_dir, f"{prefix}.png"))
        else:
            # 若维度异常需特殊处理
            raise ValueError(f"Unexpected depth data dimensions: {data.shape}")

    with h5py.File(h5_file_path, 'r') as f:
        
        def visit_func(name, node):
            if isinstance(node, h5py.Dataset):
                data = node[()]
                path_parts = name.split('/')
                dataset_dir = os.path.join(output_dir, *path_parts)
                os.makedirs(dataset_dir, exist_ok=True)

                if 'rgb' in name:
                    # RGB图像数据
                    if data.ndim == 4:
                        # (N, H, W, C)
                        for i, img_arr in enumerate(data):
                            img = Image.fromarray(img_arr.astype(np.uint8))
                            img.save(os.path.join(dataset_dir, f"{original_filename}_{i}.png"))
                    else:
                        # (H, W, C)
                        img = Image.fromarray(data.astype(np.uint8))
                        img.save(os.path.join(dataset_dir, f"{original_filename}.png"))
                elif name.split('/')[0].startswith('d'):
                    # 深度图数据 (H,W) 或 (H,W,1) 或 (N,H,W) 或 (N,H,W,1)
                    save_depth_data(data, dataset_dir, original_filename)
                else:
                    # 数值数据
                    if data.ndim <= 2:
                        # 1D或2D数据, 保存CSV
                        np.savetxt(os.path.join(dataset_dir, f"{original_filename}.csv"), data, delimiter=",")
                    else:
                        # 3D及以上维度的数据，以npy保存
                        np.save(os.path.join(dataset_dir, f"{original_filename}.npy"), data)
        
        f.visititems(visit_func)

def batch_convert_h5(root_dir):
    """
    从root_dir开始递归搜索所有的h5文件，
    对每个h5文件在其所在目录下创建extracted文件夹，将数据输出。
    文件名中保留原来的h5文件名前缀。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                h5_file_path = os.path.join(dirpath, filename)
                output_dir = os.path.join(dirpath, 'extracted')
                print(f"Extracting from {h5_file_path} to {output_dir}")
                extract_h5_datasets(h5_file_path, output_dir)


# 使用方法示例：将 "/path/to/data" 替换为你的数据所在根目录
root_directory ='/home/wyr/code/octo/robotet/datasets/baking_prep_place_butter_scene_4/mnt/raid5/data/roboset/v0.4/baking_prep/scene_4/baking_prep_place_butter_scene_4' 
batch_convert_h5(root_directory)
