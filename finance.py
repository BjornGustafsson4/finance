import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#User input data and valitization
while True:
    tickers = input("Please enter a Stock ticker: ")
    ticker_list = tickers.split()
    time_period = input("See history of the stock: 1d, 5d, 1mo, 3mo, 6mo, ytd, 2y, 5y, max: ")
    time_period = ''.join(e for e in time_period if e.isalnum())
    smal_roll= 30
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


change_df = pd.DataFrame(columns= ["ticker", "start_date", "end_date", "percent_change"])
for ticker in ticker_list:
    stock_df= yf.download(tickers= ticker, period= time_period, interval= time_interval)
    stock_df.reset_index(inplace= True)
    if 'Date' in stock_df.columns:
        stock_df= stock_df.rename(columns={'Date':'Datetime'})


    open_v = stock_df['Open'].iloc[0] #Change to first instance of today open, NOT first instance in data (this way we can see historical data vs today)
    last_v = stock_df['High'].iloc[-1]
    if last_v > open_v:
        line_fig_color= "green"
    else:
        line_fig_color= "red"
    change_prcnt = round(((last_v - open_v) / open_v) * 100, 2)


    highest = stock_df.loc[stock_df['High'].idxmax()]
    lowest = stock_df.loc[stock_df['Low'].idxmin()]


    #Simple Moving Average
    stock_df['sma_s'] = stock_df['Close'].rolling(5).mean()
    stock_df['sma_l'] = stock_df['Close'].rolling(smal_roll).mean()


    candlestick = go.Candlestick(
        x=stock_df['Datetime'],
        open=stock_df['Open'],
        high=stock_df['High'],
        low=stock_df['Low'],
        close=stock_df['Close'], 
        showlegend=False)
    volume_bar = go.Bar(
        x= stock_df['Datetime'], 
        y=stock_df['Volume'],
        showlegend=False,
        marker={
            'color': 'rgba(169,169,169,0.5)'})
    high_line = go.Scatter(
        x= stock_df['Datetime'], 
        y= stock_df['High'],
        mode= 'lines',
        name= 'USD',
        marker= {'color': line_fig_color})
    #Shows a line going from lowest low to highest high with percentage change
    low_to_high = go.Scatter(
        x= [lowest.at['Datetime'], highest.at['Datetime']], 
        y= [lowest.at['Low'], highest.at['High']],
        name=f"Change: ${round(highest.at['High'] - lowest.at['High'], 2)}<br>({round(((highest.at['High'] - lowest.at['High']) / lowest.at['High']) * 100 , 2)})%")
    #SMA short
    smas_fig = go.Scatter(
    x= stock_df['Datetime'],
    y= stock_df['sma_s'],
    mode= 'lines',
    name= 'Simple Moving Average Short',
    marker= {'color': 'lightskyblue'}
    )
    #SMA long
    smal_fig = go.Scatter(
    x= stock_df['Datetime'],
    y= stock_df['sma_l'],
    mode= 'lines',
    name= 'Simple Moving Average Long',
    marker= {'color': 'orange'}
    )
    candle_fig = go.Figure(candlestick)
    candle_fig = make_subplots(specs=[[{"secondary_y": True}]])
    candle_fig.add_trace(candlestick, secondary_y=False)
    candle_fig.add_trace(high_line, secondary_y=False)
    candle_fig.add_trace(low_to_high, secondary_y=False)
    candle_fig.add_trace(smas_fig, secondary_y=False)
    candle_fig.add_trace(smal_fig, secondary_y=False)
    candle_fig.add_trace(volume_bar, secondary_y=True)
    if time_interval != '1d':
        candle_fig.update_xaxes(
            rangebreaks=[
                { 'pattern': 'day of week', 'bounds': [6, 1]},
                { 'pattern': 'hour', 'bounds':[16,9.5]}])
    candle_fig.update_layout(
        title= f"{ticker.upper()} Report <br> {change_prcnt}%",
        xaxis_title= 'Date and Time')
    candle_fig.update_yaxes(title="Price $", secondary_y=False, showgrid=True)
    candle_fig.update_yaxes(title="Volume", secondary_y=True, showgrid=False)
    #Opening price
    candle_fig.add_hline(
        y=open_v, 
        line_dash='dash', 
        annotation_text=f"Opening price <br> {round(open_v, 3)}", 
        secondary_y=False)
    candle_fig.add_annotation(
        x= highest.at['Datetime'], 
        y=highest.at['High'], 
        text= round(highest.at['High'], 3),
        showarrow=True,
        secondary_y=False)
    candle_fig.add_annotation(
        x= lowest.at['Datetime'], 
        y= lowest.at['Low'], 
        text= round(lowest.at['Low'], 3),
        showarrow=True,
        secondary_y=False)
    candle_fig.show()
    stock_df.to_csv(f"stock_{ticker}_df.csv")


    if len(ticker_list) >= 2:
        tick_info = yf.Ticker(ticker).info
        change_lst = pd.DataFrame([{'ticker': ticker, 'start_date': stock_df['Datetime'].iloc[0], 'end_date': stock_df['Datetime'].iloc[-1], 'percent_change': change_prcnt, 'close_price':round(stock_df['Close'].iloc[-1], 2), 'revenue_per_share':tick_info['revenuePerShare'], 'de': round(tick_info['debtToEquity'], 2), 'pe_ratio':round(tick_info['trailingPE'], 2), 'bv': round(tick_info['bookValue'], 2), 'roe': (round(tick_info['returnOnEquity'], 2) * 100)}])
        change_df = pd.concat([change_df, change_lst])



#Add new stuff here for stock comparison
if len(ticker_list) >= 2:
    change_df['color_prcnt']= np.where(change_df["percent_change"]<0, 'red', 'green')

    ticker_names= ""
    for tick in ticker_list:
        ticker_names += f" {tick}"
    bars_fig = make_subplots(rows=3, cols=2, 
        subplot_titles=("Percent change ", "Closing price", "P/E Ratio", "Debt to Equity", "Return on Equity", "Book Value"))

    bars_fig.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['percent_change'], 
        marker_color= change_df['color_prcnt'],
        text= change_df['percent_change']),
        row= 1, col= 1)
    
    bars_fig.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['close_price'],
        text= change_df['close_price']),
        row= 1, col= 2)

    bars_fig.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['pe_ratio'], 
        text= change_df['pe_ratio']),
        row= 2, col= 1)

    bars_fig.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['de'], 
        text= change_df['de']),
        row= 2, col= 2)

    bars_fig.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['roe'], 
        text= change_df['roe']),
        row= 3, col= 1)

    bars_fig.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['bv'], 
        text= change_df['bv']),
        row= 3, col= 2)

    bars_fig.update_yaxes(ticksuffix="%", row=1, col=1)
    bars_fig.update_yaxes(tickprefix="$", row=1, col=2)
    bars_fig.update_yaxes(ticksuffix="%", row=3, col=1)

    pe_mean = round(change_df['pe_ratio'].mean(), 2)
    bars_fig.add_hline(
        y= pe_mean, 
        line_dash='dash', 
        annotation_text=pe_mean,
        row=2, col=1)

    bars_fig.update_layout(title_text=f"{ticker_names} stock comparison over {time_period}")
    bars_fig.update_layout(showlegend=False)
    bars_fig.show()