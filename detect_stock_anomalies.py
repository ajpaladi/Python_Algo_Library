#Script by Andrew Paladino, 02/21/2023
#the below (for now) is best suited for one ticker. More updates to come...

from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
yf.pdr_override()
import pandas as pd
import plotly.express as px
import kaleido
import numpy as np

'''
example tickers
tickers =['QQQ', 'IWY', 'IHDG', 'HEFA', 'GTO', 'SKOR', 'SPY',
             'VGT', 'VSMAX', 'BBMC', 'SLYG', 'GWX', 'VIGAX', 'TIP',
             'JSML', 'VTSAX', 'RWO', 'GSIE', 'SCHA', 'SPEU', 'SPEM',
             'FLCH', 'ANGL']
'''

def detect_anomalies(data, threshold):    #production
    threshold = threshold
    mean = np.mean(data)
    std = np.std(data)
    
    z_scores = [(y - mean) / std for y in data]
    return np.where(np.abs(z_scores) > threshold)
  
def detect_stock_anomalies(tickers, threshold, start_date, end_date = None):
    start = start_date
    if end_date == None:
        end = date.today()

    culm = pd.DataFrame()
    for t in tickers:
        print(t)
        data = pdr.get_data_yahoo(t, start, end)
        data.reset_index(inplace = True)
        data['stock'] = t
        culm = culm.append(data)
        
    anomalies_df = pd.DataFrame()
    for s in culm.stock.unique():
        df = culm[(culm.stock == s)]
        column = df['Close']
        anomalies = detect_anomalies(column, threshold)
        anomalies_s = df.iloc[anomalies]
        anomalies_df = anomalies_df.append(anomalies_s)
    return culm, anomalies_df
  
def plot_anomalies(regular_df, anomalies_df, anomaly_color):
    rdg = regular_df
    adf = anomalies_df 
    fig = px.line(regular_df, x = 'Date', y = 'Close', color = 'stock')
    fig.add_traces(
    list(px.scatter(anomalies_df, x = 'Date', y = 'Close', color_discrete_sequence=[anomaly_color]).select_traces()))
    fig.update_layout(hovermode = 'x')
    return fig.show()
  
### Examples

#reg, anomalies = detect_stock_anomalies(['QQQ'], 1, '2022-01-01')
#plot_anomalies(reg, anomalies, 'hotpink')
