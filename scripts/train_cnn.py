import os.path
import torch
import torch.optim as optim
from models import SkinDiseaseModel
import torch.nn as nn
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from argparse import ArgumentParser
from tqdm.autonotebook import tqdm
from torch.utils.tensorboard import SummaryWriter
import numpy as np
import matplotlib.pyplot as plt
import shutil
import dataset
from constants import label_mapping
import matplotlib
matplotlib.use('TkAgg')

def get_args():
    parser = ArgumentParser(description="CNN training")
    parser.add_argument("--root", "-r", type=str, default="./data", help="Root of the dataset")
    parser.add_argument("--epochs", "-e", type=int, default=100, help="Number of epochs")
    parser.add_argument("--batch-size", "-b", type=int, default=32, help="Batch size")
    parser.add_argument("--image-size", "-i", type=int, default=224, help="Image size")
    parser.add_argument("--logging", "-l", type=str, default="tensorboard")
    parser.add_argument("--trained_models", "-t", type=str, default="trained_models")
    parser.add_argument("--checkpoint", "-c", type=str, default=None)
    parser.add_argument("--patience", "-p", type=int, default=10, help="Patience for early stopping")  # Added patience
    return parser.parse_args()

def plot_confusion_matrix(writer, cm, class_names, epoch):
    figure = plt.figure(figsize=(20, 20))
    plt.imshow(cm, interpolation='nearest', cmap="ocean")
    plt.title("Confusion matrix")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    cm_normalized = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)
    threshold = cm_normalized.max() / 2.
    for i in range(cm_normalized.shape[0]):
        for j in range(cm_normalized.shape[1]):
            color = "white" if cm_normalized[i, j] > threshold else "black"
            plt.text(j, i, cm_normalized[i, j], horizontalalignment="center", color=color)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    writer.add_figure('confusion_matrix', figure, epoch)

if __name__ == '__main__':
    args = get_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device: {}".format(device))
    train_loader, test_loader = dataset.get_dataloaders(args.root, args.batch_size, use_weighted_sampling=True)
    
    if os.path.isdir(args.logging):
        shutil.rmtree(args.logging)
    if not os.path.isdir(args.trained_models):
        os.mkdir(args.trained_models)
        
    writer = SummaryWriter(args.logging)
    model = SkinDiseaseModel(num_classes=len(label_mapping.keys())).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2, verbose=True)

    if args.checkpoint:
        checkpoint = torch.load(args.checkpoint, map_location=device)
        start_epoch = checkpoint["epoch"]
        best_acc = checkpoint["best_acc"]
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
    else:
        start_epoch = 0
        best_acc = 0

    num_iters = len(train_loader)
    patience_counter = 0

    for epoch in range(start_epoch, args.epochs):
        if epoch == 5:  # Mở layer4 sau 5 epoch
            for name, param in model.model.named_parameters():
                if 'layer4' in name or 'fc' in name:
                    param.requires_grad = True
                else:
                    param.requires_grad = False
        print('Đã mở khóa layer4 để tinh chỉnh')
        model.train()
        running_loss = 0.0
        progress_bar = tqdm(train_loader, colour="green")
        for iter, (images, labels) in enumerate(progress_bar):
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss_value = criterion(outputs, labels)
            running_loss += loss_value.item()
            progress_bar.set_description("Epoch {}/{}. Iteration {}/{}. Loss {:.3f}".format(epoch+1, args.epochs, iter+1, num_iters, loss_value))
            writer.add_scalar("Train/Loss", loss_value, epoch*num_iters+iter)
            optimizer.zero_grad()
            loss_value.backward()
            optimizer.step()

        model.eval()
        all_predictions = []
        all_labels = []
        test_loss = 0.0
        with torch.no_grad():
            for images, labels in test_loader:  # Fixed test_dataloader to test_loader
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                
        test_loss /= len(test_loader)
        writer.add_scalar("Val/Loss", test_loss, epoch)
        
        plot_confusion_matrix(writer, confusion_matrix(all_labels, all_predictions), class_names=list(label_mapping.keys()), epoch=epoch)
        accuracy = accuracy_score(all_labels, all_predictions)
        print("Epoch {}: Accuracy: {}".format(epoch+1, accuracy))
        writer.add_scalar("Val/Accuracy", accuracy, epoch)
        cm = confusion_matrix(all_labels, all_predictions)
        print("\nClassification Report:")
        print(classification_report(all_labels, all_predictions, target_names=list(label_mapping.keys())))
        
        checkpoint = {
            "epoch": epoch + 1,
            "best_acc": best_acc,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict()
        }
        
        torch.save(checkpoint, "{}/last_cnn.pt".format(args.trained_models))
        
        if accuracy > best_acc:
            best_acc = accuracy
            checkpoint["best_acc"] = best_acc
            torch.save(checkpoint, os.path.join(args.trained_models, "best_cnn.pt"))
            print(f"Best model saved with accuracy: {best_acc:.3f}")
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print("Early stopping triggered!")
                break
            
        scheduler.step(test_loss)
        
    writer.close()
    print("Training complete.")