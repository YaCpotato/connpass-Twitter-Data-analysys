from datetime import datetime
import pandas as pd
import models
from models import Tweet
from setting import session


def more_shape_tweets(tweets):
    result = []
    total_imp = 0
    
    tmp_date = tweets[0].date
    for tweet in tweets:
        tweet.date = datetime.strftime(tweet.date,'%Y-%m-%d')
        total_imp += tweet.inpression
        if tweet.date != tmp_date:
            result.append({
                "date":tweet.date,
                "inpression":total_imp
            })
            total_imp = 0
            tmp_date = tweet.date 
    return result


if __name__ == '__main__':
    tweets = session.query(Tweet).distinct(Tweet.date).all()
    result = more_shape_tweets(tweets)
    for i in result:
        print(i["date"] + '   impression: ' + str(i["inpression"]))
