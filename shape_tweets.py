def by_tweet(tweets):
    result = []
    for tweet in tweets:
        if '#MLbeginners' in tweet.content or '#MLBeginners' in tweet.content:
            result.append({
                "date" : tweet.date,
                "content" : tweet.content,
                "impressions" : tweet.inpression,
                "retweets" : tweet.retweet,
                "likes" : tweet.like,
            })
        
    return result

def by_day(tweets):
    result = []
    tmp_date = tweets[0].date.date()
    day_impression = 0
    day_retweets = 0
    day_likes = 0
    for tweet in tweets:
        if '#MLbeginners' in tweet.content or '#MLBeginners' in tweet.content:
            day_impression += tweet.inpression
            day_retweets += tweet.retweet
            day_likes += tweet.like
            if tweet.date.date() != tmp_date:
                result.append({
                    "date" : tmp_date,
                    "content" : tweet.content,
                    "impressions" : day_impression,
                    "retweets" : day_retweets,
                    "likes" : day_likes,
                })
                tmp_date = tweet.date.date()
                day_impression = 0
                day_retweets = 0
                day_likes = 0
        
    return result