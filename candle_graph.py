import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def candle_graph(stock_df, time_interval, ticker):
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
    stock_df['sma_l'] = stock_df['Close'].rolling(30).mean()


    #On Balance Volume
    stock_df['obv_change'] = np.where(stock_df['Close'] > stock_df['Close'].shift(1), "+", "-")
    stock_df['obv'] = stock_df['Volume'][0]
    for index in stock_df['obv_change'].index[1:]:
        if stock_df['obv_change'][index] == '+':
            stock_df['obv'][index] = stock_df['obv'][index - 1] + stock_df['Volume'][index]
        elif stock_df['obv_change'][index] == '-':
            stock_df['obv'][index] = stock_df['obv'][index - 1] - stock_df['Volume'][index]



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
        name="Volume" ,
        marker={'color': 'rgba(169,169,169,0.5)'})
    obv = go.Scatter(
        x= stock_df['Datetime'], 
        y=stock_df['obv'],
        name="On Balance Volume" ,
        marker={'color': 'rgb(84,84,84)'},
        visible='legendonly')
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
        name=f"Change: ${round(highest.at['High'] - lowest.at['High'], 2)}<br>({round(((highest.at['High'] - lowest.at['High']) / lowest.at['High']) * 100 , 2)})%",
        visible='legendonly')
    #SMA short
    smas_fig = go.Scatter(
    x= stock_df['Datetime'],
    y= stock_df['sma_s'],
    mode= 'lines',
    name= 'Simple Moving Average Short',
    marker= {'color': 'lightseagreen'}
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
    candle_fig.add_trace(obv, secondary_y=True)
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
    return change_prcnt