import os
import numpy as np

import random

# ROOT DIR
ROOT = '/home/sun/Desktop/CRC/data/'

# NPY DIR
NPY_DIR = ROOT + 'npy/'

# LOAD ANNOTATION FILE
annotation_file = open(ROOT + 'data.txt', 'r')

# CLASS COUNT LIST
train_class_cnt = [0 for _ in range(16)]
test_class_cnt = [0 for _ in range(16)]

# READ ANNOTATION FILE LINES
datas = annotation_file.readlines()
random.shuffle(datas)

train_datas = datas[:int(len(datas)*0.9)]
test_datas = datas[int(len(datas)*0.9):]
# DATA EXTENSION
ext = '.npy'

max_list = []
min_list = []

len_list = []

train_f = open('/home/sun/Desktop/CRC/data/train_data.txt', 'w')

for idx,data in enumerate(train_datas):
    train_f.write(data)
    # len_list.append(len(data))

    name, class_idx = data.split()

    data_name = name + ext

    data_arr = np.load(NPY_DIR + data_name)

    signal = data_arr[:, 1:-1]

    len_list.append(len(signal))

    signal = np.array(signal, np.float)

    local_max = max(map(max, signal))
    local_min = min(map(min, signal))


    max_list.append(local_max)
    min_list.append(local_min)

    class_idx = int(class_idx)

    train_class_cnt[class_idx] += 1

    #print(max(data_arr))
train_f.close()
# print(max(max_list))
# print(min(min_list))

test_f = open('/home/sun/Desktop/CRC/data/test_data.txt', 'w')

for idx,data in enumerate(test_datas):
    test_f.write(data)

    name, class_idx = data.split()

    data_name = name + ext

    data_arr = np.load(NPY_DIR + data_name)

    signal = data_arr[:, 1:-1]

    len_list.append(len(signal))

    signal = np.array(signal, np.float)

    local_max = max(map(max, signal))
    local_min = min(map(min, signal))


    max_list.append(local_max)
    min_list.append(local_min)

    class_idx = int(class_idx)

    test_class_cnt[class_idx] += 1

test_f.close()

#print(len_list)
print(min(len_list))
print(max(len_list))

print(train_class_cnt)
print(test_class_cnt)
