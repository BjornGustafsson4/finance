import glob
import candle_graph
import compare
import pull
import main_func


timestamp, graph_cwd, change_df = main_func.start_var()


#changes from reading yfinance to local csv
csv_only, cwd_location = main_func.read_csv(graph_cwd)



#Data injest in different module and add custom error for when a ticker doesn't come back
#data input for pull
if not csv_only:
    ticker_list, time_period, time_interval, graph_cwd_timestamp = main_func.no_csv(graph_cwd, timestamp)


if csv_only:
    for ticker in glob.glob(f"{cwd_location}\\*.csv"):
        if "change" not in ticker:
            stock_df, ticker_name, time_interval = main_func.local(ticker)
            change_prcnt = candle_graph.candle_graph(stock_df, time_interval, ticker_name)
        else:
            continue
else:
    for ticker in ticker_list:
        stock_df = pull.stock(ticker, time_period, time_interval)
        change_prcnt = candle_graph.candle_graph(stock_df, time_interval, ticker)
        stock_df.to_csv(f"{graph_cwd_timestamp}\\{ticker}_{time_interval}.csv")
        #if len(ticker_list) >= 2:
        #    tick_info = pull.stock_info(ticker)
        #    change_df, title_str = main_func.change(ticker, change_prcnt, stock_df, tick_info, change_df, time_period)
#compare.compare(change_df, ticker_list, title_str, graph_cwd_timestamp)