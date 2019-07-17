#!/usr/bin/python

import sys
import numpy as np
import os
import json

real_stdout = sys.stdout
sys.stdout = sys.stderr  # Trick debug prints to output to stderr
# sys.path.append("..")
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
print("current path: " + os.getcwd())
# os.path.dirname("D:/obecto/scynet-gattakka-queen")
from runner.parser.keras_parser import build_model

# keras_model = run("../g3.json")

keras_json = input()
keras_model, input_metadata = build_model(json.loads(keras_json)) 
# NICE: Parsing works

print("Currently in %s" % os.getcwd())
x = np.load('data/xbnc_n.npy')
y = np.load('data/ybnc_n.npy')

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

val_loss = keras_model.evaluate(x_test, y_test)
print('score = ' + str(-val_loss), file=real_stdout)
print('display_score = ' + str(-val_loss), file=real_stdout)
# print(keras_model.predict(x_test))

# TODO: Find mock data to train on, or create real json to test
