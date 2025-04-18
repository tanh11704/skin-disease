from argparse import ArgumentParser
import numpy as np
from models import SkinDiseaseModel
import torch
import torch.nn as nn
from PIL import Image
import cv2
from torchvision import transforms
from constants import label_mapping

def get_args():
    parser = ArgumentParser(description="CNN inference")
    # parser.add_argument("--image-path", "-p", type=str, required=True, help="Path to the test image")
    parser.add_argument("--image-size", "-i", type=int, default=224, help="Image size")
    parser.add_argument("--checkpoint", "-c", type=str, default="models/best_cnn.pt", help="Path to model checkpoint")
    return parser.parse_args()

def predict_image(image_path):

    args = get_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load model
    model = SkinDiseaseModel(num_classes=len(label_mapping.keys())).to(device)
    if args.checkpoint:
        checkpoint = torch.load(args.checkpoint, map_location=device)
        model.load_state_dict(checkpoint["model"])
    else:
        print("No checkpoint found!")
        exit(0)
    model.eval()

    # Define the same test transforms as in dataset.py
    test_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    image_tensor = test_transforms(image).unsqueeze(0).to(device)  # Add batch dimension

    # Inference
    softmax = nn.Softmax(dim=1)
    with torch.no_grad():
        output = model(image_tensor)
        probs = softmax(output)

    max_idx = torch.argmax(probs, dim=1).item()
    predicted_class = list(label_mapping.keys())[max_idx]
    confidence = probs[0, max_idx].item()
    print(f"The test image is predicted as '{predicted_class}' with confidence score of {confidence:.3f}")
    return predicted_class, confidence


# if __name__ == '__main__':
#     args = get_args()
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print(f"Using device: {device}")
#
#     # Load model
#     model = SkinDiseaseModel(num_classes=len(label_mapping.keys())).to(device)
#     if args.checkpoint:
#         checkpoint = torch.load(args.checkpoint, map_location=device)
#         model.load_state_dict(checkpoint["model"])
#     else:
#         print("No checkpoint found!")
#         exit(0)
#     model.eval()
#
#     # Define the same test transforms as in dataset.py
#     test_transforms = transforms.Compose([
#         transforms.Resize(256),
#         transforms.CenterCrop(224),
#         transforms.ToTensor(),
#         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#     ])
#
#     # Load and preprocess image
#     image = Image.open(args.image_path).convert('RGB')
#     image_tensor = test_transforms(image).unsqueeze(0).to(device)  # Add batch dimension
#
#     # Inference
#     softmax = nn.Softmax(dim=1)
#     with torch.no_grad():
#         output = model(image_tensor)
#         probs = softmax(output)
#
#     max_idx = torch.argmax(probs, dim=1).item()
#     predicted_class = list(label_mapping.keys())[max_idx]
#     confidence = probs[0, max_idx].item()
#     print(f"The test image is predicted as '{predicted_class}' with confidence score of {confidence:.3f}")
#
#     # Display image with prediction
#     ori_image = cv2.imread(args.image_path)
#     cv2.imshow(f"{predicted_class}: {confidence*100:.2f}%", ori_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()