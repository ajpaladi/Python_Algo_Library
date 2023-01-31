# By Andrew Paladino, 01/31/23


from IPython.display import Image, Markdown

import pandas as pd
import numpy as np
import os
import ipywidgets as widgets
import plotly.express as px
from scipy import stats
from tqdm import tqdm_notebook as tqdm
import go_utils
from go_utils import GoProject
******************************
******************************



def detect_anomalies(data, threshold):
    threshold = threshold
    mean = np.mean(data)
    std = np.std(data)
    
    z_scores = [(y - mean) / std for y in data]
    return np.where(np.abs(z_scores) > threshold)
    
    def detect_anomalies_traffic(time, threshold):
    if time == 'day':
        traffic = day_df
        anomalies = pd.DataFrame()
        for aoi in day_df.aoi_name.unique():
            df = day_df[(day_df.aoi_name == aoi)]
            column = df['unique_count']
            anomalies_d = detect_anomalies(column, threshold)
            anomalies_day = df.iloc[anomalies_d]
            anomalies = anomalies.append(anomalies_day)
    elif time == 'night':
        traffic = night_df
        anomalies = pd.DataFrame()
        for aoi in night_df.aoi_name.unique():
            df = night_df[(night_df.aoi_name == aoi)]
            column = df['unique_count']
            anomalies_n = detect_anomalies(column, threshold)
            anomalies_night = df.iloc[anomalies_n]
            anomalies = anomalies.append(anomalies_night)
    return anomalies
    
 ### example ###

'''
day_ano = detect_anomalies_traffic('day', 3)
night_ano = detect_anomalies_traffic('night', 3)


fig = px.line(day_df, x = 'obs_date', y = 'unique_count', color = 'aoi_name',  color_discrete_sequence=px.colors.qualitative.Prism, render_mode = 'svg', title = 'Celanese Day Anomalies')
fig.add_traces(
    list(px.scatter(day_ano, x = 'obs_date', y = 'unique_count', color = 'aoi_name', color_discrete_sequence=['white']).select_traces())
)
fig.update_traces(
    marker=dict(size=8, symbol="diamond", line=dict(width=2, color="DarkSlateGrey")),
    selector=dict(mode="markers"),
)
fig.show()

'''
    
    
