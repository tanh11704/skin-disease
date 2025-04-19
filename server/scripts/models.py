import torch
import torch.nn as nn
from torchvision import models

class SkinDiseaseModel(nn.Module):
    def __init__(self, num_classes, freeze_backbone=True):
        super(SkinDiseaseModel, self).__init__()
        
        if num_classes <= 0:
            raise ValueError("num_classes must be greater than 0")
        
        self.model = models.resnet101(weights=models.ResNet101_Weights.IMAGENET1K_V1)
        
        if freeze_backbone:
            for name, param in self.model.named_parameters():
                if "fc" not in name:
                    param.requires_grad = False
        
        num_ftrs = self.model.fc.in_features
        
        self.model.fc = nn.Sequential(
            nn.Linear(num_ftrs, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        return self.model(x)