import os
import random
bg_base_path = "./pptx_static/static/bg_new"  # 背景图

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
from collections import Counter

def get_dominant_color(image_path, k=5, resize_factor=0.1):
    """
    使用 K-Means 聚类找出图片的主导颜色。

    Args:
      image_path (str): 图片文件路径。
      k (int): K-Means 聚类的簇数。寻找 k 个主要颜色。
      resize_factor (float): 调整图片大小的比例，加快处理速度。
                             设为 None 则不调整。值越小速度越快，但可能损失精度。

    Returns:
      tuple: 主导颜色的 RGB 元组 (R, G, B)，如果出错则返回 None。
    """
    img = Image.open(image_path)
    img = img.convert('RGB')

    # 可选：缩小图片以加快处理速度
    if resize_factor:
        original_size = img.size
        new_size = (int(original_size[0] * resize_factor), int(original_size[1] * resize_factor))
        # 使用 ANTIALIAS (或 Resampling.LANCZOS 在新版 Pillow 中) 进行高质量缩放
        try:
            from PIL import Image as PILImage
            resample_method = PILImage.Resampling.LANCZOS  # 较新 Pillow
        except AttributeError:
            resample_method = Image.ANTIALIAS  # 较旧 Pillow
        img = img.resize(new_size, resample_method)

    # 获取像素数据并重塑为 K-Means 可以处理的格式 (像素数 x 3通道)
    pixels = np.array(img).reshape(-1, 3)

    # 使用 K-Means 聚类
    # n_init='auto' (或 >= 10) 可以提高结果稳定性，避免陷入局部最优解
    # kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto', max_iter=100)  # max_iter 减少计算量
    # kmeans.fit(pixels)

    kmeans = MiniBatchKMeans(
        n_clusters=k,
        random_state=42,
        batch_size=2048,  # 根据内存调整
        max_iter=100,
        n_init='auto'
    )
    kmeans.fit(pixels)
    # kmeans.labels_ 包含了每个像素点所属的簇的索引
    # 我们需要找出哪个簇包含的像素点最多
    counts = Counter(kmeans.labels_)
    most_common_label = counts.most_common(1)[0][0]

    # kmeans.cluster_centers_ 包含了每个簇的中心颜色 (浮点数)
    dominant_color_float = kmeans.cluster_centers_[most_common_label]

    # 将中心颜色转为整数 RGB 元组
    dominant_color = tuple(int(c) for c in dominant_color_float)

    return dominant_color


def get_random_theme(theme=None):
    root_path = bg_base_path
    # 获取根路径下的所有文件夹
    folders = [folder for folder in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, folder))]

    # 随机选择一个文件夹
    if theme is None:
        random_folder = random.choice(folders)
    else:
        random_folder = theme

    # 返回完整的文件夹路径
    random_folder_path = os.path.join(root_path, random_folder)
    return random_folder_path


def read_md_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        content = file.read()
    return content


def get_random_file(path):
    folder_path = path

    # 获取文件夹内所有文件
    files = os.listdir(folder_path)
    files = [item for item in files if "标题页" not in item]

    # 从文件列表中随机选择一个文件
    random_file = random.choice(files)

    # 返回完整的文件路径
    random_file_path = os.path.join(folder_path, random_file)
    return random_file_path

def get_title_file(path):
    folder_path = path

    # 获取文件夹内所有文件
    files = os.listdir(folder_path)

    for file in files:
        if "标题页" in file:
            target_file = file

    # 返回完整的文件路径
    random_file_path = os.path.join(folder_path, target_file)

    return random_file_path

if __name__ == '__main__':
    # --- 使用示例 ---
    image_file = './pptx_static/static/bg_new/4/标题页.jpg' # <--- 请替换成你的 JPG 文件路径
    num_clusters = 3 # 想找出多少个主要颜色，然后取最主要的那个

    dominant_rgb = get_dominant_color(image_file, k=num_clusters, resize_factor=0.2) # 缩小到20%处理

    if dominant_rgb:
      print(f"图片的主导颜色 (RGB): {dominant_rgb}")
      hex_color = '#{:02x}{:02x}{:02x}'.format(*dominant_rgb)
      print(f"图片的主导颜色 (Hex): {hex_color}")
