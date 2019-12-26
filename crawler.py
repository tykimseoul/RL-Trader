import pandas as pd
from firebase import firebase as frb
import json
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()

columns = ['Time', 'Price', 'Net Change', 'Sell', 'Buy', 'Trading Volume']
kospi_columns = ['Time', 'Price', 'Net Change', 'Trading Volume', 'Dollar Volume']
exg_columns = ['Inquiry', 'Standard Rate', 'Net Change', 'Cash Buy', 'Cash Sell']


def crawl_intraday_data(code, time):
    intra_df = pd.DataFrame()
    for i in range(1, 41):
        print("page", i)
        page_df = pd.read_html(os.getenv("INTRADAY_DATA_SOURCE_ADDRESS").format(code=code, time=time, page=i))[0]
        intra_df = intra_df.append(page_df)
    intra_df.dropna(inplace=True)
    intra_df.drop(intra_df.columns[6], axis=1, inplace=True)
    intra_df.reset_index(inplace=True, drop=True)
    intra_df.columns = columns
    yesterday_df = pd.read_html(os.getenv("DAILY_DATA_SOURCE_ADDRESS").format(code=code))[0]
    yesterday_df.dropna(inplace=True)
    price_yesterday = yesterday_df[yesterday_df.columns[1]].iloc[1]
    intra_df['Net Change'] = intra_df['Price'] - price_yesterday
    print(intra_df)
    return intra_df


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


def crawl_intraday_kospi_data(time):
    kospi_df = pd.DataFrame()
    for i in range(1, 3):
        print("Crawling kospi page", i)
        page_df = pd.read_html(os.getenv("INTRADAY_KOSPI_SOURCE_ADDRESS").format(time=time, page=i))[0]
        kospi_df = kospi_df.append(page_df)
    kospi_df.dropna(inplace=True)
    kospi_df.drop(kospi_df.columns[3], axis=1, inplace=True)
    kospi_df.columns = kospi_columns
    yesterday_df = pd.read_html(os.getenv("DAILY_KOSPI_SOURCE_ADDRESS"))[0]
    yesterday_df.dropna(inplace=True)
    price_yesterday = yesterday_df[yesterday_df.columns[1]].iloc[1]
    kospi_df['Net Change'] = kospi_df['Price'] - price_yesterday
    kospi_df.reset_index(inplace=True, drop=True)
    print(kospi_df)
    return kospi_df


def save_intraday_kospi_data(date, df):
    firebase = frb.FirebaseApplication(os.getenv("FIREBASE_ADDRESS"), None)
    df.apply(lambda r: firebase.post('/stock/kospi/{date}'.format(date=date), json.loads(r.to_json())), axis=1)


def retrieve_intraday_kospi_data(date):
    firebase = frb.FirebaseApplication(os.getenv("FIREBASE_ADDRESS"), None)
    data = firebase.get('/stock/kospi/{date}'.format(date=date), None)
    result = pd.DataFrame.from_dict(data, orient='index')
    result = result[kospi_columns]
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
    df = crawl_intraday_data(code, '20191226230000')
    save_intraday_data(code, '12/26', df)
    retrieve_intraday_data(code, '12/26')

kospi_df = crawl_intraday_kospi_data('20191226230000')
save_intraday_kospi_data('12/26', kospi_df)
retrieve_intraday_kospi_data('12/26')

exg_df = crawl_exchange_rate()
save_exchange_data(exg_df)
retrieve_exchange_data('2019/12/24')
