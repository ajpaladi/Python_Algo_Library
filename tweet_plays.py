import pandas as pd
import threading
import tweepy

#not finished yet

#df = website[5]
#df.iloc[1]

def tweet_nfl_plays():
    hashtag1 = '#PITvsCLE'
    hashtag2 = '#HereWeGo'
    pd.set_option('max_colwidth',600)
    twitter_auth_keys = {
        "consumer_key"        : "MNn3GpSJiaqHVaUIvMR4KRyc5",
        "consumer_secret"     : "lzlHFVqNb5tLSpsyYrQBJqDEfkuQxjgPKXZreGNtZTP7QIsm4o",
        "access_token"        : "1123779250014834690-QvukGyvVNNivc84QoZIERY67pVYob3",
        "access_token_secret" : "vpT9fRzn3QnqpbqE0761b7RVc77WRBh3p4dYqVVWgQZwS"
    }
 
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
    
    website = pd.read_html('https://nytimes.stats.com/fb/pbp.asp?gamecode=20230108023&home=23&vis=5|')
    plays = pd.DataFrame()
    df = website[5]
    plays = plays.append(df)
    plays.drop_duplicates()
    plays.to_csv('plays.csv')
    #print(plays.head(1))
    to_twitter = pd.read_csv('plays.csv')
    for i in to_twitter['0'].head(2):          
        string = i
        print(string)
        if 'TOUCHDOWN' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'Penalty' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'extra point' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'field goal attempt' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'INTERCEPTED' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'TIMEOUT' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'FUMBLE' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif 'sacked' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
        elif '2 pt conversion' in string:
            tweet = i + '\n' + hashtag1 +  '\n' + hashtag2
            try:
                status = api.update_status(status = tweet)
                print(f'Successfully tweeted: {tweet}')
            except tweepy.errors.Forbidden as e:
                print(f'Error: {e}')
    threading.Timer(5, tweet_nfl_plays).start()
    return tweet_nfl_plays

#tweet_nfl_plays()
