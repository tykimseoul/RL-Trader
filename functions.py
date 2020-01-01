import numpy as np
import math
from pandas_datareader import data
from time import gmtime
from time import strftime
import pandas as pd


def intraday_from_csv(start, end):
    df = pd.read_csv('kodex.csv')
    df.dropna(inplace=True)
    df['Time'] = df['Time'].str[:-3]

    return df.loc[(df['Date'] >= start) & (df['Date'] <= end)]['End'].tolist()


# prints formatted price
def format_price(n):
    return ("-" if n < 0 else '') + "{0:.0f}".format(abs(n))


def format_time(t):
    return strftime("%H:%M:%S", gmtime(t))


# returns the vector containing stock data from a fixed file
def get_stock_data(key, start, end):
    # # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    # panel_data = data.DataReader(key, 'yahoo', start, end)
    #
    # # Getting just the adjusted closing prices. This will return a Pandas DataFrame
    # # The index in this DataFrame is the major index of the panel_data.
    # return panel_data['Close'].tolist()
    data = intraday_from_csv(start, end)
    print('data length: ', len(data))
    return data


# returns the sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# returns an an n-day state representation ending at time t
def get_state(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]  # pad with t0
    res = [sigmoid(block[i + 1] - block[i]) for i in range(n - 1)]

    return np.array([res])
