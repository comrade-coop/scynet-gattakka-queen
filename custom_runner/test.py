import sys
import numpy as np
import os

sys.path.append("..")
from runner.parser.keras_parser import run

keras_model = run("../genome.json")
# NICE: Parsing works

print("Currently in %s" % os.getcwd())
x = np.load('../data/xbnc_n.npy')
y = np.load('../data/ybnc_n.npy')

print('Loaded')
print(x.shape)
print(y.shape)

test_split = 0.1
data_size = len(x)
test_data_len = int(test_split * data_size)

x_train = x[test_data_len:]
y_train = y[test_data_len:]

x_test = x[:test_data_len]
y_test = y[:test_data_len]

keras_model.summary()
keras_model.fit(x_train, y_train, epochs=1, validation_split=0.0)

# TODO: Find mock data to train on, or create real json to test
