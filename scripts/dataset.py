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
                    self.image_paths.append(os.path.join(class_dir, img_name))
                    self.labels.append(class_idx)
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label
    
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
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
    weights = 1.0 / class_counts
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
    
    if use_weighted_sampling:
        train_sampler = create_weighted_sampler(train_dataset)
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=batch_size,
            sampler=train_sampler,
            num_workers=4,
            pin_memory=True
        )
    else:
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=4,
            pin_memory=True
        )
    
    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    return train_loader, test_loader