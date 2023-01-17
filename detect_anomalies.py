from scipy import stats
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

def detect_anomalies(data):
    threshold = 1.5
    mean = np.mean(data)
    std = np.std(data)
    
    z_scores = [(y - mean) / std for y in data]
    return np.where(np.abs(z_scores) > threshold)

# extract column
column = day_results['unique_count_day']

# detect anomalies
anomalies = detect_anomalies(column)

# print anomalous rows

#anomaly df
anomolies = df.iloc[anomalies]

#regular df
df = day_results

#Plot both using:

fig = px.line(day_results, x = 'obs_date', y = 'unique_count_day', render_mode = 'svg', color_discrete_sequence=['blue'], title = 'Anomaly Detection: Giant Grocery Story DMV')
fig.add_traces(
    list(px.scatter(anomolies, x = 'obs_date', y = 'unique_count_day', color_discrete_sequence=['red']).select_traces())
)
