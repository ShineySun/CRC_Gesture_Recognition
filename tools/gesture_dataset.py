import os

import numpy as np
from torch.utils.data import Dataset

class GestureData(Dataset):
    def __init__(self, root_dir='/home/sun/Desktop/CRC/data/', train = True):
        self.root_dir = root_dir
        self.npy_dir = root_dir + 'npy/'
        self.anno_file = None
        self.extension = '.npy'
        self.x_min = 650.0
        self.x_max = 4000.0

        if train:
            train_f = open(self.root_dir + "train_data.txt", 'r')
            self.anno_file = train_f.readlines()
        else:
            test_f = open(self.root_dir + "test_data.txt", 'r')
            self.anno_file = test_f.readlines()

    def __len__(self):
        return len(self.anno_file)

    def __getitem__(self, idx):
        file_name, class_label = self.anno_file[idx].split()

        raw_data = np.load(self.npy_dir + file_name + self.extension)

        # normalize
        gesture_data = np.array(raw_data[:, 1:-1], np.float)

        gesture_data = (gesture_data - self.x_min) / (self.x_max - self.x_min)

        # padding
        if len(gesture_data) <= 50:
            gesture_data = np.append(gesture_data, np.zeros((50-len(gesture_data), 5)), axis=0)

        gesture_data = np.array([gesture_data], np.float)

        #print(gesture_data)

        class_label = np.array(int(class_label))

        return {'gesture_data' : gesture_data, 'class_label' : class_label}
