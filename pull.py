import pandas as pd
import yfinance as yf

def stock(ticker, time_period, time_interval):
    stock_df= yf.download(tickers= ticker, period= time_period, interval= time_interval)
    stock_df.reset_index(inplace= True)
    if 'Date' in stock_df.columns:
        stock_df= stock_df.rename(columns={'Date':'Datetime'})
    return stock_df
    

def local_data(ticker_location):
    data_df = pd.read_csv(ticker_location)
    return data_df

    
def stock_info(ticker):
    tick_info = yf.Ticker(ticker).info
    return tick_info