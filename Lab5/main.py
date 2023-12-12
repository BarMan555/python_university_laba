import os
import numpy as np
import pandas as pd
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as functional
from torchvision import transforms
from matplotlib import pyplot as plt
from PIL import Image
from typing import Tuple, Any


def load_data(csv_path : str) -> list:
    """Def for load dataset and output list"""
    dframe = pd.read_csv(csv_path, delimiter=",", names=["Absolute path", "Relative path", "Class"])
    list_ = dframe["Absolute path"].to_list()
    return list_


def separation_data(images : list) -> Tuple[list, list, list]:
    """Separation data lika a train, test and valid"""
    train_data = images[0:int(len(images) * 0.8)]
    test_data = images[int(len(images) * 0.8) : int(len(images) * 0.9)]
    valid_data = images[int(len(images) * 0.9) : len(images)]
    return train_data, test_data, valid_data


class dataset(torch.utils.data.Dataset):
    def __init__(self, list_, transform:Any=None) -> None:
        self.dataset = list_
        self.transform = transform


    def __len__(self) -> int:
        return len(self.dataset)
    

    def __getitem__(self,index : int) -> Tuple[torch.tensor, int]:
        path_to_image = self.dataset.iloc[index, 0]
        label = self.dataset.iloc[index, 1]
        # image = cv2.cvtColor(cv2.imread(path_to_image), cv2.COLOR_BGR2RGB)
        img = Image.open(path_to_image)
        img = self.transform(img)
        return img, label
    

def transform_data(train_list, test_list, valid_list) -> Tuple[dataset, dataset, dataset]:
    """Transform dataset"""
    custom_transforms = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]
    )
    train_data = dataset(train_list, transform=custom_transforms)
    test_data = dataset(test_list, transform=custom_transforms)
    valid_data = dataset(valid_list, transform=custom_transforms)
    return train_data, test_data, valid_data


class CNN(nn.Module):
    def __init__(self) -> None:
        super(CNN,self).__init__()
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(3,16,kernel_size=3, padding=0,stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.layer2 = nn.Sequential(
            nn.Conv2d(16,32, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
            )
        
        self.layer3 = nn.Sequential(
            nn.Conv2d(32,64, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        
        self.fc1 = nn.Linear(576,10)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(10,2)
        self.relu = nn.ReLU()
        
        
    def forward(self,x):
        output = self.layer1(x)
        output = self.layer2(output)
        output = self.layer3(output)
        output = output.view(output.size(0),-1)
        output = self.relu(self.fc1(output))
        output = self.fc2(output)
        return output