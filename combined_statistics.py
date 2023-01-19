import pandas as pd
import threading
import tweepy
import plotly.express as px
import numpy as np

#team_names = ['Cowboys', 'Niners', 'Ravens', 'Browns', 'Bengals', 'Bills', 'Chiefs', 'Vikings',
#              'Dolphins', 'Chargers', 'Seahawks', 'Steelers', 'Jaguars', 'Giants', 'Eagles']
#team_prefixes = ['DAL', 'SF', 'BAL', 'CLE', 'CIN', 'BUF', 'KC', 'MIN',
#                 'MIA', 'LAC', 'SEA', 'PIT', 'JAX', 'NYG', 'PHI']

def combined_offense(team_names, team_prefixes, stat):
    combined_o = pd.DataFrame()

    for name, prefix in zip(team_names, team_prefixes):
        offense = get_statistics(name, prefix, 'offense', stat)
        combined_o = combined_o.append(offense)

    combined_o = combined_o.reset_index()
    return combined_o

def combined_defense(team_names, team_prefixes, stat):
    combined_d = pd.DataFrame()
    
    for name, prefix in zip(team_names, team_prefixes):
        defense = get_statistics(name, prefix, 'defense', stat)
        combined_d = combined_d.append(defense)
    
    combined_d = combined_d.reset_index() 
    return combined_d

###example###
#combined_defense(['Steelers', 'Niners'], ['PIT', 'SF'], 'max')
