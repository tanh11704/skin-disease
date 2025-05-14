import os
import cv2
import albumentations as A
from tqdm import tqdm

# Định nghĩa thư mục Train
train_dir = "./SkinDisease/train"

# Mục tiêu số lượng mẫu tối thiểu cho mỗi lớp
target_samples = 1000

# Định nghĩa pipeline tăng cường dữ liệu
transform = A.Compose([
    A.Rotate(limit=30, p=0.5),  # Xoay ảnh ngẫu nhiên trong khoảng -30 đến 30 độ
    A.HorizontalFlip(p=0.5),    # Lật ngang ảnh
    A.VerticalFlip(p=0.5),      # Lật dọc ảnh
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),  # Thay đổi độ sáng và độ tương phản
    A.GaussNoise(p=0.2),        # Thêm nhiễu Gaussian
])

# Kiểm tra xem thư mục train có tồn tại không
if not os.path.exists(train_dir):
    raise FileNotFoundError(f"Thư mục {train_dir} không tồn tại. Vui lòng kiểm tra lại đường dẫn.")

# Duyệt qua từng lớp trong thư mục Train
for category in tqdm(os.listdir(train_dir), desc="Processing classes"):
    category_path = os.path.join(train_dir, category)
    
    if not os.path.isdir(category_path):
        continue  # Bỏ qua nếu không phải thư mục
    
    # Đếm số lượng ảnh hiện tại trong lớp
    images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f)) and 'aug' not in f]
    num_images = len(images)
    
    print(f"Class {category}: {num_images} samples")
    
    # Nếu số lượng ảnh nhỏ hơn mục tiêu, tạo thêm ảnh
    if num_images < target_samples:
        num_to_generate = target_samples - num_images
        print(f"Generating {num_to_generate} additional samples for {category}...")
        
        # Duyệt qua các ảnh hiện có và tạo ảnh mới
        for img_name in images:
            img_path = os.path.join(category_path, img_name)
            image = cv2.imread(img_path)
            if image is None:
                print(f"Không thể đọc ảnh {img_path}, bỏ qua...")
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Tạo ảnh mới cho đến khi đủ số lượng
            for i in range(num_to_generate // num_images + 1):
                augmented = transform(image=image)
                augmented_image = augmented["image"]
                new_img_name = f"{os.path.splitext(img_name)[0]}_aug_{i}.jpg"
                cv2.imwrite(os.path.join(category_path, new_img_name), cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
                
                num_images += 1
                if num_images >= target_samples:
                    break
            if num_images >= target_samples:
                break

print("Data augmentation completed! 🚀")