import pandas as pd
from firebase import firebase as frb
import json
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()

columns = ['Time', 'Current', 'AD', 'ADR', 'Trading Volume', 'Dollar Volume']
exg_columns = ['Inquiry', 'Standard Rate', 'Net Change', 'Cash Buy', 'Cash Sell']


def crawl_intraday_data(code):
    intra_df = pd.DataFrame()
    for i in range(1, 22):
        print("page", i)
        page_df = pd.read_html(os.getenv("INTRADAY_DATA_SOURCE_ADDRESS").format(code=code, page=i))[10]
        intra_df = intra_df.append(page_df)

    crawled_date = intra_df[intra_df.columns[0]].iloc[0].split(' ')[0]
    intra_df[intra_df.columns[0]] = intra_df[intra_df.columns[0]].str.split(' ', n=1, expand=True)[1]
    intra_df.sort_values(intra_df.columns[0], inplace=True)
    intra_df.drop_duplicates(subset=intra_df.columns[0], keep='first', inplace=True)
    intra_df.reset_index(inplace=True, drop=True)
    intra_df.columns = columns
    intra_df['AD'] = intra_df['Current'] - intra_df.iloc[0]['Current']
    intra_df['ADR'] = intra_df['ADR'] / 100
    print(intra_df)
    print(intra_df.shape)
    return intra_df, crawled_date


def save_intraday_data(code, date, df):
    firebase = frb.FirebaseApplication(os.getenv("FIREBASE_ADDRESS"), None)
    df.apply(lambda r: firebase.post('/stock/{code}/{date}'.format(code=code, date=date), json.loads(r.to_json())), axis=1)


def retrieve_intraday_data(code, date):
    firebase = frb.FirebaseApplication(os.getenv("FIREBASE_ADDRESS"), None)
    data = firebase.get('/stock/{code}/{date}'.format(code=code, date=date), None)
    result = pd.DataFrame.from_dict(data, orient='index')
    result = result[columns]
    result.reset_index(inplace=True, drop=True)
    print(result)
    return result


def crawl_exchange_rate():
    exg_df = pd.DataFrame()
    for i in range(1, 41):
        print("page", i)
        page_df = pd.read_html(os.getenv("EXCHANGE_RATE_DATA_SOURCE_ADDRESS").format(page=i))[0]
        page_df.drop(page_df.columns[4:8], axis=1, inplace=True)
        page_df.columns = exg_columns
        exg_df = exg_df.append(page_df)

    exg_df.sort_values(exg_df.columns[0], inplace=True)
    exg_df['Inquiry'] = pd.to_numeric(exg_df['Inquiry'].str[:-1])
    exg_df.set_index('Inquiry', inplace=True)
    print(exg_df)
    return exg_df


def save_exchange_data(df):
    firebase = frb.FirebaseApplication(os.getenv("FIREBASE_ADDRESS"), None)
    today = date.today().strftime("%Y/%m/%d")
    df.apply(lambda r: firebase.post('/exchange/{date}'.format(date=today), json.loads(r.to_json())), axis=1)


def retrieve_exchange_data(date):
    firebase = frb.FirebaseApplication(os.getenv("FIREBASE_ADDRESS"), None)
    data = firebase.get('/exchange/{date}'.format(date=date), None)
    result = pd.DataFrame.from_dict(data, orient='index')
    result.reset_index(inplace=True, drop=True)
    result.index = result.index + 1
    print(result)


codes = json.loads(os.getenv("RELEVANT_STOCK_CODES"))
for code in codes:
    df, date = crawl_intraday_data(code)
    save_intraday_data(code, date, df)
    retrieve_intraday_data(code, date)

exg_df = crawl_exchange_rate()
save_exchange_data(exg_df)
retrieve_exchange_data('2019/12/24')
