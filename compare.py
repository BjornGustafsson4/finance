from plotly.subplots import make_subplots
import plotly.graph_objects as go
from os import system

def compare(change_df, ticker_list, title_str, graph_cwd_timestamp):
    ticker_names= ""
    for tick in ticker_list:
        ticker_names += f" {tick}"
    bars_fig_1 = make_subplots(rows=1, cols=2, 
        subplot_titles=("Percent change ", "Closing price"))
    bars_fig_2 = make_subplots(rows=1, cols=2, 
        subplot_titles=("Price to Earnings", "Price to Sales"))
    bars_fig_3 = make_subplots(rows=1, cols=2, 
        subplot_titles=("Return on Equity", "Debt to Equity"))
    bars_fig_1.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['percent_change'], 
        marker_color= change_df['color_prcnt'],
        text= change_df['percent_change']),
        row= 1, col= 1)
    bars_fig_1.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['close_price'],
        marker_color= change_df['color_prcnt'],
        text= change_df['close_price']),
        row= 1, col= 2)
    bars_fig_2.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['pe_ratio'], 
        text= change_df['pe_ratio']),
        row= 1, col= 1)
    bars_fig_2.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['ps'], 
        text= change_df['ps']),
        row= 1, col= 2)
    bars_fig_3.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['roe'], 
        text= change_df['roe']),
        row= 1, col= 1)
    bars_fig_3.add_trace(go.Bar(
        x= change_df['ticker'],
        y= change_df['de'], 
        text= change_df['de']),
        row= 1, col= 2)

    bars_fig_1.update_yaxes(ticksuffix="%", row=1, col=1)
    bars_fig_1.update_yaxes(tickprefix="$", row=1, col=2)
    bars_fig_3.update_yaxes(ticksuffix="%", row=1, col=1)

    pe_mean = round(change_df['pe_ratio'].mean(), 2)
    bars_fig_2.add_hline(
        y= pe_mean, 
        line_dash='dash', 
        annotation_text=pe_mean,
        row=1, col=1)
    ps_mean = round(change_df['ps'].mean(), 2)
    bars_fig_2.add_hline(
        y= ps_mean, 
        line_dash='dash', 
        annotation_text=ps_mean,
        row=1, col=2)


    bars_fig_1.update_layout(title_text=f"{ticker_names} stock comparison {title_str}")
    bars_fig_1.update_layout(showlegend=False)
    bars_fig_2.update_layout(showlegend=False)
    bars_fig_3.update_layout(showlegend=False)


    #Save graphs in folder
    bars_fig_1.write_html(f"{graph_cwd_timestamp}\\bar_fig_1.html")
    bars_fig_2.write_html(f"{graph_cwd_timestamp}\\bar_fig_2.html")
    bars_fig_3.write_html(f"{graph_cwd_timestamp}\\bar_fig_3.html")


    #creates a new HTML file to run all individual graphs on one page
    html_graphs = open(f"{graph_cwd_timestamp}\\comparison.html", "w")
    html_graphs.write(f"<html lang='en'>\n<head>\n<meta charset='utf-8'>\n<title>Stock comparison</title>\n</head>\n<body style='text-align: center'>\n<embed type='text/html' src='bar_fig_1.html' width='1300' height='500'>\n<embed type='text/html' src='bar_fig_2.html' width='1300' height='500'>\n<embed type='text/html' src='bar_fig_3.html' width='1300' height='500''>\n</body>\n</html>")
    html_graphs.close()
    system(f"{graph_cwd_timestamp}\\comparison.html")