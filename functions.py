import math
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
