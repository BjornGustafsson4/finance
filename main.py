import pandas as pd
import numpy as np
import os
import glob
import candle_graph
import compare
import pull



#changes from reading yfinance to local csv
while True:
    csv_only = input("Do you want to read previously saved local data (Yes/No): ")
    if csv_only.lower() in ["yes", "y", "true"]:
        csv_only = True
        break
    elif csv_only.lower() in ["no", "n", "false"]:
        csv_only = False
        break
    else:
        continue


timestamp = pd.Timestamp.now().strftime('%Y_%m_%d_%H_%M')
graph_cwd = f"{os.getcwd()}\\graphs"


change_df = pd.DataFrame(columns= ["ticker", "percent_change"])
#Data injest in different module and add custom error for when a ticker doesn't come back
#data input for pull
if not csv_only:
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
        if time_period.lower() in ("1d 5d 1mo 3mo 6mo ytd 2y 5y max"):
            break
        else:
            #Creates files to save data and graphs
            graph_cwd_timestamp = f"{graph_cwd}\\{timestamp}"
            if os.path.exists(graph_cwd) == False:
                os.mkdir(graph_cwd)
                if os.path.exists(graph_cwd_timestamp) == False:
                    os.mkdir(graph_cwd_timestamp)
            else:
                if os.path.exists(graph_cwd_timestamp) == False:
                    os.mkdir(graph_cwd_timestamp)
            continue


if csv_only:
    folder = input("Please enter folder name: ")
    cwd_location = f"{graph_cwd}\\{folder}"
    os.system(f"{cwd_location}\\comparison.html")
    for ticker in glob.glob(f"{cwd_location}\\*.csv"):
        stock_df = pull.local_data(ticker)
        ticker_name = ticker.rsplit("\\", 1)[1]
        ticker_name = ticker_name.rsplit(".")[0]
        if ticker_name != "change":
            ticker_name, time_interval = ticker_name.split("_")
            change_prcnt = candle_graph.candle_graph(stock_df, time_interval, ticker_name)
        else:
            continue
else:
    for ticker in ticker_list:
        stock_df = pull.stock(ticker, time_period, time_interval)
        change_prcnt = candle_graph.candle_graph(stock_df, time_interval, ticker)
        stock_df.to_csv(f"{graph_cwd_timestamp}\\{ticker}_{time_interval}.csv")
    if len(ticker_list) >= 2:
        tick_info = pull.stock_info(ticker)
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

        #Creates a list and date for titles  !! EXPAND THIS TO CANDLE_GRAPH !!
        if time_period != '1d':
            title_str = f"from {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[0]} to {str(stock_df['Datetime'].iloc[-1]).split(' ', 1)[0]}"
        else:
            title_str = f"on {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[0]} from {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[1].split('-')[0]} to {str(stock_df['Datetime'].iloc[-1]).split(' ', 1)[1].split('-')[0]}"

        #Compares tickers
        compare.compare(change_df, ticker_list, title_str, graph_cwd_timestamp)