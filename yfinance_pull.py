import yfinance as yf
import pandas as pd
import numpy as np

def stock(ticker, time_period, time_interval):
    stock_df= yf.download(tickers= ticker, period= time_period, interval= time_interval)
    stock_df.reset_index(inplace= True)
    if 'Date' in stock_df.columns:
        stock_df= stock_df.rename(columns={'Date':'Datetime'})
    return stock_df
    
def stock_info(ticker, stock_df, change_prcnt):
    tick_info = yf.Ticker(ticker).info
    pd.DataFrame(tick_info).to_csv("temp_for_error.csv")
    change_lst = pd.DataFrame([{
        'ticker': ticker, 
        'percent_change': change_prcnt, 
        'close_price':round(stock_df['Close'].iloc[-1], 2), 
        'revenue_per_share':tick_info['revenuePerShare'], 
        'de': round(tick_info['debtToEquity']/100, 2), 
        'pe_ratio':round(tick_info['trailingPE'], 2), 
        'ps': round(tick_info['priceToSalesTrailing12Months'], 2), 
        'roe': (round(tick_info['returnOnEquity'], 2) * 100)}])
    change_df = pd.concat([change_df, change_lst])
    change_df['color_prcnt']= np.where(change_df["percent_change"]<0, 'red', 'green')
    return change_df