import math
from time import gmtime
from time import strftime
import pandas as pd


# prints formatted price
def format_price(n):
    return ("-" if n < 0 else '') + "{0:.0f}".format(abs(n))


def format_time(t):
    return strftime("%H:%M:%S", gmtime(t))


# returns the vector containing stock data from a fixed file
def get_stock_data(name, start, end):
    stock_data = import_csv(name, start, end)
    kospi_data = import_csv('kospi', start, end)

    return stock_data, kospi_data


def import_csv(name, start, end):
    df = pd.read_csv(name + '.csv')
    df.dropna(inplace=True)
    df['Time'] = df['Time'].str[:-3]

    data = df.loc[(df['Date'] >= start) & (df['Date'] <= end)]['End'].tolist()
    print('data length: ', len(data))
    return data


# returns the sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))
