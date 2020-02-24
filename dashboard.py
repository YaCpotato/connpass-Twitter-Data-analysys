# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import models
from models import Tweet
from setting import session
from datetime import datetime
import csv
import sys
from matplotlib import pyplot as plt
import seaborn as sns

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

# 使いまわされそうなものは関数にする
def is_within_time(time,start,end):
    #time = datetime.strftime(time,'%Y-%m-%d')
    # FormatTimeだけだと年月が1990-1-1になるので現実の年月を使えるようにする
    date = datetime.strptime(time,'%Y-%m-%d')
    return start < date < end

def shape_tweets(tweets):
    result = []
    total_impressions = 0
    total_retweets = 0
    total_likes = 0
    total_tag_tweets = 0
    detail = []
    tmp_date = tweets[0].date
    for tweet in tweets:
        tweet.date = datetime.strftime(tweet.date,'%Y-%m-%d')
        if '#MLbeginners' in tweet.content and is_within_time(tweet.date,datetime(2020,1,27),datetime(2020,2,26)): #1'2019-10-02 00:00','2019-10-27 13:00' #3 '2019-12-14 16:30','2020-01-18 12:00'
            total_impressions += tweet.inpression
            total_retweets += tweet.retweet
            total_likes += tweet.like
            total_tag_tweets += 1
            detail.append(tweet)
        
            # 最初、もしくは前の日付と違ったら、tweet_dateの更新を行い、描画用オブジェクトにappend。
            if tweet.date != tmp_date:                #tweet_date = datetime.strptime(tweet.date,'%Y-%m-%d')
                result.append({
                    "date" : tweet.date,
                    "total_impressions" : total_impressions,
                    "total_retweets" : total_retweets,
                    "total_impressions" : total_impressions,
                    "total_likes" : total_likes,
                    "detail" : detail
                })
                total_impressions = 0
                total_retweets = 0
                total_likes = 0
                total_tag_tweets = 0
                detail = []
        
    return result

tweets = session.query(Tweet).distinct(Tweet.date).all()

shaped_tweets = shape_tweets(tweets)

ml_date = []
ml_impression = []
ml_retweet = []
ml_like = []
for twi in shaped_tweets:
    ml_date.append(twi["date"])
    ml_impression.append(twi["total_impressions"])
    ml_retweet.append(twi["total_retweets"])
    ml_like.append(twi["total_likes"])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='example-graph-1',
                figure={
                    'data': [
                        {'x': ml_date, 'y': ml_impression, 'type': 'bar', 'name': 'SF'},
                    ],
                    'layout': {
                        'title': 'インプレッション数'
                    }
                }
            )
        ]
    )
])])


if __name__ == '__main__':
    app.run_server(debug=True)
