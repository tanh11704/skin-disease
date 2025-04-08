import os
import shutil
import random
from sklearn.model_selection import train_test_split

# Định nghĩa thư mục nguồn và đích
source_dir = "data/ĐACN1"  # Thư mục chứa dữ liệu gốc
train_dir = "data/train"   # Thư mục train
test_dir = "data/test"     # Thư mục test

# Tạo thư mục train và test nếu chưa có
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Duyệt qua từng lớp bệnh (Herpes_Zoster, Urticaria, Varicella)
for category in os.listdir(source_dir):
    category_path = os.path.join(source_dir, category)
    
    if not os.path.isdir(category_path):
        continue  # Bỏ qua nếu không phải thư mục
    
    # Tạo thư mục cho train và test
    os.makedirs(os.path.join(train_dir, category), exist_ok=True)
    os.makedirs(os.path.join(test_dir, category), exist_ok=True)

    # Lấy danh sách tất cả ảnh trong thư mục
    images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]

    # Chia dữ liệu thành train (80%) và test (20%)
    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)

    # Di chuyển ảnh vào thư mục train
    for img in train_images:
        shutil.move(os.path.join(category_path, img), os.path.join(train_dir, category, img))

    # Di chuyển ảnh vào thư mục test
    for img in test_images:
        shutil.move(os.path.join(category_path, img), os.path.join(test_dir, category, img))

print("Chia dataset hoàn tất! 🚀")