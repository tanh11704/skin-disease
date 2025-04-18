# scripts/count_data.py
import os
from collections import defaultdict
from constants import label_mapping  # Import label_mapping từ infer.py
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Sử dụng backend không cần GUI
import numpy as np

def count_data_in_directory(data_dir):
    """
    Đếm số lượng file trong mỗi class trong thư mục dữ liệu.
    Args:
        data_dir (str): Đường dẫn đến thư mục (train hoặc test)
    Returns:
        dict: Số lượng file cho mỗi class
    """
    class_counts = defaultdict(int)
    
    for class_name in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path):
            num_files = len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])
            class_counts[class_name] = num_files
    
    return class_counts

def print_data_summary(train_counts, test_counts):
    """
    In tóm tắt số lượng dữ liệu cho từng class và tổng.
    Args:
        train_counts (dict): Số lượng file trong tập train
        test_counts (dict): Số lượng file trong tập test
    """
    print("\n=== Tóm tắt số lượng dữ liệu ===")
    
    total_train = sum(train_counts.values())
    total_test = sum(test_counts.values())
    
    print(f"{'Class':<20} {'Tên tiếng Việt':<30} {'Train':<10} {'Test':<10} {'Tổng':<10}")
    print("-" * 85)
    
    for class_name in sorted(label_mapping.keys()):
        train_count = train_counts.get(class_name, 0)
        test_count = test_counts.get(class_name, 0)
        total = train_count + test_count
        vietnamese_name = label_mapping[class_name]
        print(f"{class_name:<20} {vietnamese_name:<30} {train_count:<10} {test_count:<10} {total:<10}")
    
    print("-" * 85)
    print(f"{'Tổng':<20} {'':<30} {total_train:<10} {total_test:<10} {total_train + total_test:<10}")

def plot_data_distribution(train_counts, test_counts):
    """
    Vẽ biểu đồ phân bố dữ liệu cho từng class.
    Args:
        train_counts (dict): Số lượng file trong tập train
        test_counts (dict): Số lượng file trong tập test
    """
    # Lấy danh sách class và số lượng
    classes = sorted(label_mapping.keys())
    train_values = [train_counts.get(cls, 0) for cls in classes]
    test_values = [test_counts.get(cls, 0) for cls in classes]
    
    # Thiết lập vị trí cột
    x = np.arange(len(classes))  # Vị trí trên trục x
    width = 0.35  # Độ rộng của cột
    
    # Tạo biểu đồ
    plt.figure(figsize=(15, 8))
    plt.bar(x - width/2, train_values, width, label='Train', color='skyblue')
    plt.bar(x + width/2, test_values, width, label='Test', color='salmon')
    
    # Tùy chỉnh biểu đồ
    plt.xlabel('Class')
    plt.ylabel('Số lượng mẫu')
    plt.title('Phân bố dữ liệu theo Class (Train và Test)')
    plt.xticks(x, classes, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    # Hiển thị biểu đồ
    plt.show()

if __name__ == "__main__":
    # Đường dẫn đến thư mục train và test
    train_dir = "../data/train"
    test_dir = "../data/test"
    
    # Đếm số lượng file
    train_counts = count_data_in_directory(train_dir)
    test_counts = count_data_in_directory(test_dir)
    
    # In bảng tóm tắt
    print_data_summary(train_counts, test_counts)
    
    # Vẽ biểu đồ
    plot_data_distribution(train_counts, test_counts)