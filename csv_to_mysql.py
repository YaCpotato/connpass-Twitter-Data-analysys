# -*- coding:utf-8 -*-
import models
from models import Tweet
from setting import session
from datetime import datetime
import csv
import sys

def csv_import_to_mysql(path):
    """
    csvファイルのパスを受け取り、データベースに保存するメソッド
    """
    with open('secret/'+path) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            tweets = Tweet()
            tweets.tweet_id = row[0]
            tweets.content = row[2]
            tweets.date = datetime.strptime(row[3],'%Y-%m-%d %H:%M %z')#2019-11-27 10:35 +0000
            tweets.inpression = round(float(row[4]))
            tweets.engagement = round(float(row[5]))
            tweets.retweet = round(float(row[7]))
            tweets.reply = round(float(row[8]))
            tweets.like = round(float(row[9]))
            tweets.profile_click = round(float(row[10]))
            tweets.url_click = round(float(row[11]))
            tweets.hashtag_click = round(float(row[12]))
            tweets.detail_click = round(float(row[13]))
            session.add(tweets)
            session.commit()
    return

if __name__ == "__main__":
    args = sys.argv
    csv_import_to_mysql(args[1])
