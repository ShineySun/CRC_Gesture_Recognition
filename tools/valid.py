import torch
from torch.utils.data import DataLoader

from gesture_dataset import GestureData
from model import Net, Net2

import matplotlib.pyplot as plt

def make_data(data):
    # normalize factor
    x_min = 650.0
    x_max = 4000.0

    gesture_data = np.array(data[:, 1:], np.float)

def run(state_dict_path, data):

    # model
    model = Net()

    # load parameters
    model.load_state_dict(torch.load(state_dict_path))

    # model.cuda()
    model = model.cuda()

    # model.eval()
    model.eval()

    data = data.cuda()

    pred = model()


    return None

# print(next(iter(train_loader))['gesture_data'].shape)

# Model
model = Net().cuda()

# Loss
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

# Container
train_loss_container = []
test_loss_container = []
accuracy_container = []

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

    with torch.no_grad():
        for data in test_loader:
            data['gesture_data'] = data['gesture_data'].cuda().float()
            data['class_label'] = data['class_label'].cuda().long()

            pred = model(data['gesture_data'])
            loss = criterion(pred, data['class_label'].long())

            correct_prediction = torch.argmax(pred, 1) == data['class_label']

            test_loss += loss.item() / total_test_batch

            if correct_prediction:
                acc_point += 1

    test_loss_container.append(test_loss)
    accuracy_container.append(acc_point / total_test_batch)

    acc_ratio = acc_point / total_test_batch

    print('Accuracy Ratio : {}%'.format(acc_ratio))

    if acc_ratio > best_acc_ratio:
        PATH = '/home/hci/Desktop/CRC_Gesture_Recognition/output/' + str(epoch) + "_state_dict_model.pt"
        torch.save(model.state_dict(), PATH)

plt.plot(train_loss_container)
plt.plot(test_loss_container)
plt.plot(accuracy_container)
plt.show()
