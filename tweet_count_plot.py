from datetime import datetime, timedelta
import os
import pandas as pd
from datetime import date
import snscrape.modules.twitter as sntwitter
import itertools
from datetime import datetime, timedelta
from datetime import date

def tweet_count_plot(start_date, end_date, search_term):
    delta = timedelta(days=1)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dates = []
    tweet_count = []
    links = pd.DataFrame()
    while start <= end:
        dates.append(start.date())
        start += delta
    for d in dates:
        end_d = d + delta
        os.system(f"snscrape --since {d} twitter-search '{search_term} until:{end_d}' > tweet-count.txt")
        if os.stat("tweet-count.txt").st_size == 0:
            counter = 0
        else:
            links_df = pd.read_csv('tweet-count.txt', names=['link'])
            links = links.append(links_df)
            counter = links_df.size
        tweet_count.append(counter)

    df = pd.DataFrame({'Date': dates, 'Counts': tweet_count})
    df['Date'] = pd.to_datetime(df['Date'])
    merged_df = pd.merge(df, links, left_index=True, right_index=True)
    return df
  
#### Example 
### tweet_count('Dronebase', '2023-02-07', '2023-02-08')
### tweets.plot(x = 'Date', y = 'Counts', figsize = (10,7))
