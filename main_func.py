import pandas as pd
import numpy as np
import os
import pull



def start_var():
    timestamp = pd.Timestamp.now().strftime('%Y_%m_%d_%H_%M')
    graph_cwd = f"{os.getcwd()}\\graphs"
    change_df = pd.DataFrame(columns= ["ticker", "percent_change"])
    return timestamp, graph_cwd, change_df



def read_csv(graph_cwd):
    while True:
        csv_only = input("Do you want to read previously saved local data (Yes/No): ")
        if csv_only.lower() in ["yes", "y", "true"]:
            csv_only = True
            folder = input("Please enter folder name: ")
            cwd_location = f"{graph_cwd}\\{folder}"
            os.system(f"{cwd_location}\\comparison.html")
            break
        elif csv_only.lower() in ["no", "n", "false"]:
            csv_only = False
            cwd_location = graph_cwd
            return csv_only, cwd_location
        else:
            continue


def no_csv(graph_cwd, timestamp):
    while True:
        tickers = input("Please enter one or more stock tickers: ")
        tickers_list = tickers.split() #split on other things? comma, space, comma+space
        ticker_list = []
        for tick in tickers_list:
            tick = ''.join(e for e in tick if e.isalnum())
            ticker_list.append(tick)
        time_period = input("See history of the stock: 1d, 5d, 1mo, 3mo, 6mo, ytd, 2y, 5y, max: ")
        time_period = ''.join(e for e in time_period if e.isalnum())
        #save = input("Do you want to save your graphs? (y/n): ")
        if time_period.lower() == "1d":
            time_interval ='1m'
        elif time_period == '5d':
            time_interval = '15m'
        elif time_period.lower() in "1mo 3mo":
            time_interval ='1h'
        else: 
            time_interval= '1d'
        if time_period.lower() in ["1d", "5d", "1mo", "3mo", "6mo", "ytd", "2y", "5y", "max"] and len(ticker_list) > 0:
            #Creates files to save data and graphs
            graph_cwd_timestamp = f"{graph_cwd}\\{timestamp}"
            if os.path.exists(graph_cwd) == False:
                os.mkdir(graph_cwd)
            if os.path.exists(graph_cwd_timestamp) == False:
                os.mkdir(graph_cwd_timestamp)
                return ticker_list, time_period, time_interval, graph_cwd_timestamp
        else:
            continue


def local(ticker):
    stock_df = pull.local_data(ticker)
    ticker_name = ticker.rsplit("\\", 1)[1]
    ticker_name = ticker_name.rsplit(".")[0]
    ticker_name, time_interval = ticker_name.split("_")
    return stock_df, ticker_name, time_interval


def change(ticker, change_prcnt, stock_df, tick_info, change_df, time_period):
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
    #Creates a list and date for titles 
    if time_period != '1d':
        title_str = f"from {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[0]} to {str(stock_df['Datetime'].iloc[-1]).split(' ', 1)[0]}"
    else:
        title_str = f"on {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[0]} from {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[1].split('-')[0]} to {str(stock_df['Datetime'].iloc[-1]).split(' ', 1)[1].split('-')[0]}"

    return change_df, title_str
