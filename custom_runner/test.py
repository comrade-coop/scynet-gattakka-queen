print("HELLO WORLD")
import sys
import numpy as np
import os

sys.path.append("..")
from runner.parser.keras_parser import run
real_stdout = sys.stdout
# sys.stdout = sys.stderr  # Trick debug prints to output to stderr

keras_model = run("../g3.json")

# keras_json = input()
# keras_model = run(keras_json)
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

val_loss = keras_model.evaluate(x_test, y_test)
print('score = ' + str(-val_loss), file=real_stdout)
print(keras_model.predict(x_test))

# TODO: Find mock data to train on, or create real json to test
