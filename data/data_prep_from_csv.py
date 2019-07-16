import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

df = pd.read_csv('ETH_train_df.csv')

data = df.as_matrix()
data = np.array(data)

print('the shape of the data is', data.shape)

close = data[:, 4]
high = data[:,2]
low = data[:,1]
open = data[:,3]
close = np.array([float(x) for x in close])
high = np.array([float(x) for x in high])
low = np.array([float(x) for x in low])
open = np.array([float(x) for x in open])
avg_price = (high + low) / 2

price_signal_buy = close.copy()
price_signal_hold = close.copy()

y = []

stop_loss = 99.5 / 100
take_profit = 101.0 / 100
future_time = 48

for i in range(len(close) - future_time):
        price_up_or_down = False
        for j in range(future_time):
                if low[i + j] < close[i] * stop_loss:
                        y.append([0])
                        price_up_or_down = True
                        break
                elif high[i + j] > close[i] * take_profit:
                        y.append([1])
                        price_up_or_down = True
                        break

        if price_up_or_down == False:
                y.append([0])

        if y[-1][0] == 1:
                price_signal_hold[i] = np.nan
        if y[-1][0] == 0:
                price_signal_buy[i] = np.nan

                
# print('plt')
# plt.plot(price_signal_buy, '.-g')
# plt.plot(price_signal_hold, '.-b')
# # plt.plot(high, '-y')
# # plt.plot(low, '-r')
# plt.show()

# 40 is when all the indicators stop returning nan
indicator_offset = 40
y = np.array(y[indicator_offset:])


timeperiod = 14
adx = talib.ADX(high, low, close, timeperiod=timeperiod) / 100
adxr = talib.ADXR(high, low, close, timeperiod=timeperiod) / 100
ar = talib.AROONOSC(high, low, timeperiod=timeperiod) / 200 + .5
dx = talib.DX(high, low, close, timeperiod=timeperiod) / 100
mdi = talib.MINUS_DI(high, low, close, timeperiod=timeperiod) / 100
pdi = talib.PLUS_DI(high, low, close, timeperiod=timeperiod) / 100
rsi = talib.RSI(close, timeperiod=timeperiod) / 100
willr = talib.WILLR(high, low, close, timeperiod=timeperiod) / -100
fastk, fastd = talib.STOCHRSI(close, timeperiod=timeperiod, fastk_period=5, fastd_period=3, fastd_matype=0)
fastk /= 100
fastd /= 100

x = []
for i in range(len(close)):
        if i < indicator_offset:
                continue
        val = [adx[i],adxr[i],ar[i],dx[i],mdi[i],pdi[i],rsi[i],willr[i],fastk[i],fastd[i]]
        x.append(val)

x = np.array(x[:-future_time])

print('the shape of x is', x.shape)
print('the shape of y is', y.shape)

np.save('ready_data/xbnc_n.npy', np.nan_to_num(x))
np.save('ready_data/ybnc_n.npy', np.nan_to_num(y))

print('data is saved!')


