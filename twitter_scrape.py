import os
from datetime import date
import pandas as pd
import snscrape

def total_tweets(search_term, start_date, end_date):
    os.system(f"snscrape --since {start_date} twitter-search '{search_term} until:{end_date}' > result-tweets.txt")
    if os.stat("result-tweets.txt").st_size == 0:
        counter = 0
    else:
        df = pd.read_csv('result-tweets.txt', names=['link'])
        counter = df.size

    print("Number of Tweets : " + str(counter))
    
    return total_tweets
  
  def tweet_content(max_results, search_term, start_date, end_date):
    extracted_tweets = "snscrape --format '{content!r}'" + f" --max-results {max_results} --since {start_date} twitter-search '{search_term} until:{end_date}' > extracted-tweets.txt"
    os.system(extracted_tweets)
    if os.stat("extracted-tweets.txt").st_size == 0:
        print('No Tweets Found')
    else:
        df = pd.read_csv('extracted-tweets.txt', names=['content'])
        for row in df['content'].iteritems():
            print(row)
    return tweet_content
