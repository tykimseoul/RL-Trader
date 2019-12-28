import pandas as pd


def intraday_from_csv(start, end):
    df = pd.read_csv('kodex.csv')
    df.dropna(inplace=True)
    df['Time'] = df['Time'].str[:-3]

    return df.loc[(df['Date'] >= start) & (df['Date'] <= end)]['End'].tolist()
