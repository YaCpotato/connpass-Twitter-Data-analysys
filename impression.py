import models
from models import Tweet
from setting import session
from datetime import datetime
import csv
import sys
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="ticks")
plt.style.use('seaborn-whitegrid')

if __name__ == '__main__':
    impressions = []
    date = []
    ml_impressions = []
    ml_date = []
    tweets = session.query(Tweet).distinct(Tweet.date).all()
    """
    for tweet in tweets:
        date.append(tweet.date)
        impressions.append(tweet.inpression)
    
    plt.bar(date,impressions)
    plt.savefig('impression.png')
    """

    for tweet in tweets:
        if '#MLbeginners' in tweet.content:
            ml_date.append(tweet.date)
            ml_impressions.append(tweet.inpression)
    
    plt.bar(ml_date,ml_impressions)
    plt.savefig('ml_tweets_impression.png')
    
            