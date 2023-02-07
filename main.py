import pandas as pd
import numpy as np
import os
import candle_graph
import compare
import pull
import main_func as mf

#changes from reading yfinance to local csv
csv_only = True


change_df = pd.DataFrame(columns= ["ticker", "percent_change"])
#Data injest in different module and add custom error for when a ticker doesn't come back
#data input for pull
while True:
    tickers = input("Please enter one or more stock tickers: ")
    tickers_list = tickers.split() #split on other things? comma, space, comma+space
    ticker_list = []
    for tick in tickers_list:
        tick = mf.input_val(tick)
        ticker_list.append(tick)
    time_period = mf.input_val(input("See history of the stock: 1d, 5d, 1mo, 3mo, 6mo, ytd, 2y, 5y, max: "))
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
        continue


#Creates files to save data and graphs
timestamp = pd.Timestamp.now().strftime('%Y_%m_%d_%H_%M')
graph_cwd = f"{os.getcwd()}\\graphs"
graph_cwd_timestamp = f"{graph_cwd}\\{timestamp}"
if os.path.exists(graph_cwd) == False:
    os.mkdir(graph_cwd)
    if os.path.exists(graph_cwd_timestamp) == False:
        os.mkdir(graph_cwd_timestamp)
else:
    if os.path.exists(graph_cwd_timestamp) == False:
        os.mkdir(graph_cwd_timestamp)


if csv_only:
    folder = input("Please enter folder name: ")
    cwd_location = f"{graph_cwd}\\{folder}"
for ticker in ticker_list:
    if not csv_only:
        stock_df = pull.stock(ticker, time_period, time_interval)
    else:
        stock_df = pull.local_data(ticker, cwd_location)
    
    change_prcnt = candle_graph.candle_graph(stock_df, time_interval, ticker)

    if len(ticker_list) >= 2 and csv_only == False:
        tick_info = pull.stock_info(ticker)
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


#Creates a list and date for titles  !! EXPAND THIS TO CANDLE_GRAPH !!
if time_period != '1d':
    title_str = f"from {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[0]} to {str(stock_df['Datetime'].iloc[-1]).split(' ', 1)[0]}"
else:
    title_str = f"on {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[0]} from {str(stock_df['Datetime'].iloc[0]).split(' ', 1)[1].split('-')[0]} to {str(stock_df['Datetime'].iloc[-1]).split(' ', 1)[1].split('-')[0]}"


compare.compare(change_df, ticker_list, title_str, graph_cwd_timestamp)