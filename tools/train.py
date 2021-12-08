import torch
from torch.utils.data import DataLoader

from gesture_dataset import GestureData
from model import Net, Net2, Net3

import numpy as np
import matplotlib.pyplot as plt

epochs = 200
best_acc_ratio = .0

# DataLoader
train_dataset = GestureData()
test_dataset = GestureData(train=False)

train_loader = DataLoader(train_dataset, batch_size = 16, shuffle = True)
test_loader = DataLoader(test_dataset, batch_size = 1, shuffle = False)

# print(next(iter(train_loader))['gesture_data'].shape)

# Model
model = Net3().cuda()

# Loss
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Container
train_loss_container = []
test_loss_container = []
accuracy_container = []
train_accuracy_container = []

for epoch in range(epochs):

    model.train()

    train_loss = 0
    total_train_batch = len(train_loader)

    for data in train_loader:
        optimizer.zero_grad()

        data['gesture_data'] = data['gesture_data'].cuda().float()
        data['class_label'] = data['class_label'].cuda().long()

        #print(data['class_label'])

        pred = model(data['gesture_data'])
        loss = criterion(pred, data['class_label'].long())

        loss.backward()
        optimizer.step()

        train_loss += loss.item() / total_train_batch

    train_loss_container.append(train_loss)
    print('* Epoch : ', '%04d' % (epoch+1), 'Loss : ', '{:.9f}'.format(train_loss))

    model.eval()

    test_loss = 0
    acc_point = 0

    total_test_batch = len(test_loader)

    validation_arr = []

    validation_arr = np.zeros((16,16))

    with torch.no_grad():
        for data in test_loader:
            # print(data['gesture_data'].shape)
            #print(data['gesture_data'])
            data['gesture_data'] = data['gesture_data'].cuda().float()
            data['class_label'] = data['class_label'].cuda().long()

            pred = model(data['gesture_data'])

            loss = criterion(pred, data['class_label'].long())

            correct_prediction = torch.argmax(pred, 1) == data['class_label']

            validation_arr[data['class_label'].item()][torch.argmax(pred,1)] += 1

            test_loss += loss.item() / total_test_batch

            if correct_prediction:
                acc_point += 1

    acc_ratio = acc_point / total_test_batch

    # for var in validation_arr:
    #     print(var/np.linalg.norm(var)*100)

    test_loss_container.append(test_loss)
    accuracy_container.append(acc_point / total_test_batch)

    print('Accuracy Ratio : {}%'.format(acc_point / total_test_batch))

    # if acc_ratio > best_acc_ratio:
    #     PATH = "/home/sun/Desktop/CRC/output/model1/" + str(epoch) + "_state_dict_model.pt"
    #     torch.save(model.state_dict(), PATH)

plt.plot(train_loss_container)
plt.plot(test_loss_container)
plt.plot(accuracy_container)
plt.show()
