# Stock Analysis

Stock Analysis is a program that analyzes historical data and produces interactive graphs with pandas and plotly while using yfinance to retrieve the data.  
This program needs minimal input (one or more stock tickers and length of historical time) and outputs individual graphs for each ticker, with multiple trendlines.  
If multiple tickers are given in the input they will then be compared against each other to assess if the stock is overvalued or undervalued

Future updates:
    -- Modularize program
    -- Complete offline data reading
    - Add XG Boost Classifer model to help predict future movement
    - Add a UI