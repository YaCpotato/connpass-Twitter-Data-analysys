from datetime import datetime
import pandas as pd
import models
from models import Tweet
from setting import session

def shape_tweets(tweets):
    for tweet in tweets:
        tweet.date = datetime.strftime(tweet.date,'%Y-%m-%d')
    
    return tweets

if __name__ == '__main__':
    tweets = session.query(Tweet).distinct(Tweet.date).all()
    result = shape_tweets(tweets)
    
    for i in result:
        print(i.date + str(i.inpression))