import os
import h5py
import numpy as np
from PIL import Image

def save_depth_data(data, dataset_dir, prefix):
    # 将NaN或Inf替换为0，避免无效值引发警告
    data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    
    # 尝试去掉单通道维度
    # 如果是(H,W,1) -> (H,W)
    # 或 (N,H,W,1) -> (N,H,W)
    if data.ndim == 3 and data.shape[-1] == 1:
        data = np.squeeze(data, axis=-1)
    elif data.ndim == 4 and data.shape[-1] == 1:
        # 对 (N,H,W,1) 情况下先reshape
        # 假设该情况存在的话:
        # 如果是 (N,H,W,1) → (N,H,W)
        data = np.squeeze(data, axis=-1)

    # 现在预期的深度数据应为(H,W)或(N,H,W)
    if data.ndim == 3:
        # 多帧深度图 (N, H, W)
        # 为确保转换无问题，将数据裁剪到0-65535范围内
        data = np.clip(data, 0, 65535)
        for i in range(data.shape[0]):
            depth_img = data[i].astype(np.uint16)
            # 检查维度
            if depth_img.ndim != 2:
                # 如果出现异常维度，则无法作为图像保存
                return False
            img = Image.fromarray(depth_img, mode='I;16')
            img.save(os.path.join(dataset_dir, f"{prefix}_{i}.png"))
        return True
    elif data.ndim == 2:
        # 单帧深度图 (H, W)
        data = np.clip(data, 0, 65535)
        depth_img = data.astype(np.uint16)
        img = Image.fromarray(depth_img, mode='I;16')
        img.save(os.path.join(dataset_dir, f"{prefix}.png"))
        return True
    else:
        # 非预期维度，无法作为深度图保存
        return False

def extract_h5_datasets(h5_file_path, output_dir):
    """
    输出规则：
    - 保留原h5文件名为前缀 original_filename
    - 'rgb'包含在数据集名称中 -> RGB图像数据，PNG
    - 路径中任意一节以'd'开头(例如d_left, d_right) -> 尝试作为深度图数据保存为PNG
      若无法匹配(H,W)或(N,H,W)等格式，则回退到普通数据保存规则
    - 其他数值数据:
      * 1D或2D数组: CSV
      * 3D及以上数组: NPY
    """
    os.makedirs(output_dir, exist_ok=True)
    original_filename = os.path.splitext(os.path.basename(h5_file_path))[0]

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
                elif any(part.startswith('d') for part in path_parts):
                    # 深度图数据尝试
                    if not save_depth_data(data, dataset_dir, original_filename):
                        # 如果返回False，则不能作为深度图保存
                        # 按普通数据方式保存
                        save_as_regular_data(data, dataset_dir, original_filename)
                else:
                    # 普通数据
                    save_as_regular_data(data, dataset_dir, original_filename)
        
        f.visititems(visit_func)

def save_as_regular_data(data, dataset_dir, original_filename):
    """ 将数据按照普通数据规则保存 """
    if data.ndim <= 2:
        # 1D或2D数据, 保存CSV
        np.savetxt(os.path.join(dataset_dir, f"{original_filename}.csv"), data, delimiter=",")
    else:
        # 3D及以上维度的数据，以npy保存
        np.save(os.path.join(dataset_dir, f"{original_filename}.npy"), data)


def batch_convert_h5(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                h5_file_path = os.path.join(dirpath, filename)
                output_dir = os.path.join(dirpath, 'extracted')
                print(f"Extracting from {h5_file_path} to {output_dir}")
                extract_h5_datasets(h5_file_path, output_dir)

# 示例：
# root_directory = "/path/to/data"
# batch_convert_h5(root_directory)
