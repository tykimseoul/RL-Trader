import numpy as np
import math
from pandas_datareader import data
from time import gmtime
from time import strftime


# prints formatted price
def format_price(n):
    return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))


def format_time(t):
    return strftime("%H:%M:%S", gmtime(t))


# returns the vector containing stock data from a fixed file
def get_stock_data(key, start, end):
    # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    panel_data = data.DataReader(key, 'yahoo', start, end)

    # Getting just the adjusted closing prices. This will return a Pandas DataFrame
    # The index in this DataFrame is the major index of the panel_data.
    return panel_data['Close'].tolist()


# returns the sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# returns an an n-day state representation ending at time t
def get_state(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]  # pad with t0
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))

    return np.array([res])
