import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt


#User input data and valitization
today = pd.Timestamp(dt.datetime.now().date().strftime("%Y-%m-%d"))
while True:
    ticker = input("Please enter a Stock ticker: ")
    ticker = ''.join(e for e in ticker if e.isalnum())
    time_period = input("See history of the stock: 1d, 5d, 1mo, 3mo, 6mo, ytd, max: ")
    time_period = ''.join(e for e in time_period if e.isalnum())
    if time_period.lower() in ("1d 5d"): 
        time_interval ='1m'
    elif time_period.lower() in "1mo 3mo":
        time_interval ='1h'
    else: 
        time_interval= '1d'
    if time_period.lower() in ("1d 5d 1mo 3mo 6mo ytd max"):
        break
    else:
        continue


stock_df = yf.download(tickers= ticker, period= time_period, interval= time_interval)
stock_df.reset_index(inplace= True)
if 'Date' in stock_df.columns:
    stock_df['Datetime'] = stock_df['Date']


open_v = stock_df['Open'].iloc[0] #Change to first instance of today open, NOT first instance in data (this way we can see historical data vs today)
last_v = stock_df['High'].iloc[-1]
if last_v > open_v:
    line_fig_color= "green"
else:
    line_fig_color= "red"
change_prcnt = round(((last_v - open_v) / open_v) * 100, 2)


highest = stock_df.loc[stock_df['High'].idxmax()]
lowest = stock_df.loc[stock_df['Low'].idxmin()]

#Change from px.line to go.scatter so that rangebreaks will work! or this is only for 1d graph and everything else gets something different
#Could we graph by index on x axis then change the index number to date?
line_fig = px.line(stock_df, 
                x=stock_df['Datetime'], 
                y=stock_df['High'], 
                labels={'Datetime': 'Date and Time', 'High': 'USD$'},
                title= f"{ticker.upper()} High Report <br> {change_prcnt}%")
line_fig.update_traces(line_color=line_fig_color)
if time_period.lower() in ("1d 5d"): 
    line_fig.add_hline(y=open_v, line_dash='dash', annotation_text=f"Opening price <br> {round(open_v, 3)}")
line_fig.add_annotation(x= highest.at['Datetime'], y=highest.at['High'], 
                    text= round(highest.at['High'], 3),
                    showarrow=True)
line_fig.show()



candle_fig = go.Figure(data=[go.Candlestick(x=stock_df['Datetime'],
                open=stock_df['Open'],
                high=stock_df['High'],
                low=stock_df['Low'],
                close=stock_df['Close'], 
                line=dict(width=1))])
candle_fig.update_xaxes(
    rangebreaks=[
        { 'pattern': 'day of week', 'bounds': [6, 1]},
        { 'pattern': 'hour', 'bounds':[16,9.5]}
    ]
)
candle_fig.update_layout(
    title= f"{ticker.upper()} Report <br> {change_prcnt}%",
    yaxis_title= 'USD$',
    xaxis_title= 'Date and Time'
)
if time_period.lower() in ("1d 5d"): 
    candle_fig.add_hline(y=open_v, line_dash='dash', annotation_text=f"Opening price <br> {round(open_v, 3)}")
candle_fig.add_annotation(x= highest.at['Datetime'], y=highest.at['High'], 
                    text= round(highest.at['High'], 3),
                    showarrow=True)
candle_fig.add_annotation(x= lowest.at['Datetime'], y= lowest.at['Low'], 
                    text= round(lowest.at['Low'], 3),
                    showarrow=True,
                    )
candle_fig.show()