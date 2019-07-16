import datetime
from time import sleep
from binance.client import Client

keys = {'APIKey':'rZAdNHbB9hxfner9tmJsklIILxs1MxTOOCyjRMvu3G4YazvC7sPDM9WjMGt4qWQg',
       'SecretKey':'LBNRVG0BxfIj7EnA07YzeE6eFB7x7QGvAUx51cLq7Z1xZpAkK7uGhBfwoDqgbJ7z'}

client = Client(keys['APIKey'], keys['SecretKey'])

ETH_train = client.get_historical_klines(symbol='ETHBTC', interval= '1m', start_str= '2019.01.01', end_str= '2019.03.31')
ETH_test = client.get_historical_klines(symbol='ETHBTC', interval= '1m', start_str= '2019.04.01', end_str= '2019.05.01')

import numpy as np
import pandas as pd

ETH_train_df= pd.DataFrame(ETH_train, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
ETH_test_df= pd.DataFrame(ETH_test, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

ETH_train_df['Open time']= pd.to_datetime(ETH_train_df['Open time'], unit='ms')
ETH_test_df['Open time']= pd.to_datetime(ETH_test_df['Open time'], unit='ms')

ETH_train_df.set_index('Open time', inplace=True)
ETH_test_df.set_index('Open time', inplace=True)

ETH_train_df.head()

# ETH_train_df.drop('Close time','Quote asset volume', axis=1).head()
ETH_train_df = ETH_train_df.rename_axis('time')[['Low','High','Open','Close','Volume']]
ETH_test_df = ETH_test_df.rename_axis('time')[['Low','High','Open','Close','Volume']]

ETH_train_df.head()

ETH_train_df.index = (ETH_train_df.index.astype(np.int64) / 10**9).astype(np.int64)
ETH_test_df.index = (ETH_test_df.index.astype(np.int64) / 10**9).astype(np.int64)

ETH_test_df.tail()

ETH_train_df.to_csv(r'ETH_train_df.csv')
ETH_test_df.to_csv(r'ETH_test_df.csv')

ETH_train_df = pd.read_csv('ETH_train_df.csv')
ETH_test_df = pd.read_csv('ETH_test_df.csv')

ETH_test_df['Close'].values
