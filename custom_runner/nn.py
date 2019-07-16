import tensorflow.keras as keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import random
from keras_parser import run

model = run("../genome.json")


x = np.load('data/ready_data/xbnc_n.npy')
y = np.load('data/ready_data/ybnc_n.npy')



# x = np.load('data/xcs.npy')
# y = np.load('data/ycs.npy')

# import matplotlib.pyplot as plt
# # plt.plot(x[:, 4])
# # plt.plot(x[:, 5])
# # plt.plot(x[:, 6])
# # plt.plot(y)
# print(len(y[y == 1]) / len(y))
# print(len(y[y == 0]) / len(y))
# # plt.show()
# input()
# # x = x[:, [4,5,6]]



# # equal + and -
# new_x = []
# new_y = []
# for i in range(len(y)):
#     if y[i] == 1:
#         new_x.append(x[i])
#         new_y.append(y[i])

# count = 0
# positive_ys = len(new_y)
# for i in range(len(y)):
#     if count == positive_ys:
#         break
#     if y[i] == 0:
#         new_x.append(x[i])
#         new_y.append(y[i])
#         count += 1

# x = np.array(new_x)
# y = np.array(new_y)



print('load')
print(x.shape)
print(y.shape)

# print('before', len(y[y == 1]), len(y[y == 0]))
# data = np.array([[x[i], y[i]] for i in range(x.shape[0])])
# random.shuffle(data)

# x = np.array([data[i][0] for i in range(len(data))])
# y = np.array([data[i][1] for i in range(len(data))])
# print(len(y[y > .5]))

# print('after', len(y[y == 1]), len(y[y == 0]))

# print(len(y[y == 1]) / len(y) * 100)
# input()


print('test')
print(x.shape)
print(y.shape)

test_split = 0.1
data_size = len(x)
test_data_len = int(test_split * data_size)

x_train = x[test_data_len:]
y_train = y[test_data_len:]

x_test = x[:test_data_len]
y_test = y[:test_data_len]

model.fit(x_train, y_train, epochs=1, validation_split=0.0)


# test data
val_loss = model.evaluate(x_test, y_test)
print('error', val_loss)

y_predicted = model.predict(x_test)
y_predicted[y_predicted > 0.5]  = 1
y_predicted[y_predicted <= 0.5] = 0

tp = 0
fp = 0
tn = 0
fn = 0

for i in range(len(y_test)):
    if y_test[i] == 1 and y_predicted[i] == 1:
        tp += 1
    elif y_test[i] == 1 and y_predicted[i] == 0:
        fn += 1
    elif y_test[i] == 0 and y_predicted[i] == 1:
        fp += 1
    elif y_test[i] == 0 and y_predicted[i] == 0:
        tn += 1


print(50*'-')
print('\nresults:')
print('True Possitive', "{:.2f}%".format((tp / (tp + fp + .0001)) * 100))
print('False Possitive', "{:.2f}%".format((fp / (tp + fp + .0001)) * 100))
print('True Negative', "{:.2f}%".format((tn / (tn + fn + .0001)) * 100))
print('False Negative', "{:.2f}%".format((fn / (tn + fn + .0001)) * 100))

print('True Possitive', tp)
print('False Possitive', fp)
print('True Negative', tn)
print('False Negative', fn)


import time
model.save('models/model_{:.0f}.h5'.format(time.time()))
print('model saved')
