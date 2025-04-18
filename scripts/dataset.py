import PIL
import torch
from torch.utils.data import Dataset
import os
from PIL import Image
import numpy as np
from torchvision import transforms
from constants import label_mapping

class SkinDiseaseDataset(Dataset):
    def __init__(self, data_dir, transform=None, mode='train'):
        self.data_dir = data_dir
        self.mode = mode
        self.class_names = list(label_mapping.keys())
        self.transform = transform
        
        self.image_paths = []
        self.labels = []
        
        for class_idx, class_name in enumerate(self.class_names):
            class_dir = os.path.join(data_dir, mode, class_name)
            if not os.path.exists(class_dir):
                continue
                
            for img_name in os.listdir(class_dir):
                if img_name.endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(class_dir, img_name)
                    try:
                        Image.open(img_path).verify()  # Kiểm tra file
                        self.image_paths.append(img_path)
                        self.labels.append(class_idx)
                    except (PIL.UnidentifiedImageError, IOError):
                        print(f"Cảnh báo: File hỏng {img_path}")
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        try:
            image = Image.open(img_path).convert('RGB')
        except (PIL.UnidentifiedImageError, IOError):
            print(f"Cảnh báo: Bỏ qua file lỗi {img_path}")
            return None, None  # Trả về None để lọc sau

        if self.transform:
            image = self.transform(image)
            
        return image, label
    
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

test_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def get_datasets(data_dir):
    train_dataset = SkinDiseaseDataset(
        data_dir=data_dir,
        transform=train_transforms, 
        mode='train'
    )
    
    test_dataset = SkinDiseaseDataset(
        data_dir=data_dir,
        transform=test_transforms, 
        mode='test'
    )
    
    return train_dataset, test_dataset

def create_weighted_sampler(dataset):
    class_counts = np.zeros(len(label_mapping))
    for _, label in dataset:
        class_counts[label] += 1
    
    class_counts = np.maximum(class_counts, 1)
    weights = 1.0 / (class_counts ** 0.5)
    sample_weights = np.array([weights[label] for _, label in dataset])
    sample_weights = torch.from_numpy(sample_weights).float()
    sample_weights = sample_weights / sample_weights.sum() * len(sample_weights)
    
    return torch.utils.data.WeightedRandomSampler(
        sample_weights, 
        len(sample_weights), 
        replacement=True
    )
    
def get_dataloaders(data_dir, batch_size=32, use_weighted_sampling=True):
    train_dataset, test_dataset = get_datasets(data_dir)

    train_dataset.image_paths = [p for p, l in zip(train_dataset.image_paths, train_dataset.labels) if p is not None]
    train_dataset.labels = [l for l in train_dataset.labels if l is not None]
    test_dataset.image_paths = [p for p, l in zip(test_dataset.image_paths, test_dataset.labels) if p is not None]
    test_dataset.labels = [l for l in test_dataset.labels if l is not None]

    if use_weighted_sampling:
        train_sampler = create_weighted_sampler(train_dataset)
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=batch_size,
            sampler=train_sampler,
            num_workers=4,
            pin_memory=True,
            drop_last=True
        )
    else:
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=4,
            pin_memory=True,
            drop_last=True
        )
    
    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    return train_loader, test_loader