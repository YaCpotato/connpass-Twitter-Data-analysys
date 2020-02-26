# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
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
"""
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
"""
def shape_tweets_delta(tweets):
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
"""
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
"""

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
#1'2019-10-02 00:00','2019-10-27 13:00' 
#22019/11/08(金) 21:00 〜2019/12/04(水) 11:30
#3 '2019-12-14 16:30','2020-01-18 12:00'
#4atetime(2020,1,27),datetime(2020,2,26)
events_number = [0,1,2,3]
events_date = [
    [2019,10,2,2019,10,27],
    [2019,11,8,2019,12,4],
    [2019,12,14,2020,1,18],
    [2020,1,27,2020,2,26]
]
subject = ['タグ付きツイート数','インプレッション数','RT数','いいね数']

app.layout = html.Div(children=[
    html.Div(
        style={ 'width':'100vw',
                'minHeight':'15vh',
                'margin':'0 auto',
                'text-align':'center'
                },
        children=[
        html.Span(
            style={'margin':'16px','fontSize':'28px','fontWeight':'bold'},
            children='Machine Learning for Beginners! Twitter分析ダッシュボード'),
        ]
    ),
    html.Div(
        style={ 'width':'100vw',
                'minHeight':'15vh',
                'margin':'0 auto',
                'text-align':'left',
                'display':'flex'
                },
        children=[
        dcc.Dropdown(
            id='event-number',
            style={'width':'10vw','marginRight':'8px'},
            options=[{'label': '第'+str(i + 1)+'回', 'value': i} for i in events_number],
            value=events_number[0]
        ),
        dcc.Dropdown(
                id='subject',
                style={'width':'15vw','marginRight':'8px'},
                options=[{'label': i, 'value': i} for i in subject],
                value=subject[0]
            ),
        ]
    ),
    html.Div(
        style={'display':'flex'},
        children=[
        html.Div(
            style={'width':'50vw'},
            children=[
            dcc.Graph(id='graph-with-dropdown')   
            ]
        ),
        html.Div(
            id='tweet-list',
            style={'width':'50vw','maxHeight':'80vh','overflowY':'scroll'},
            children=[]
        )
    ]
)])

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    [Input('event-number','value')])
def update_display_event(event_number):
    tweets = session.query(Tweet.content,Tweet.date,Tweet.inpression,Tweet.retweet,Tweet.like).\
    filter(
        Tweet.date >= datetime(events_date[int(event_number)][0],events_date[int(event_number)][1],events_date[int(event_number)][2]),
        Tweet.date < datetime(events_date[int(event_number)][3],events_date[int(event_number)][4],events_date[int(event_number)][5]),
    ).\
    distinct(Tweet.date).all()

    shaped_tweets = shape_tweets_delta(tweets)

    ml_date = []
    ml_content = []
    ml_impression = []
    ml_retweet = []
    ml_like = []
    for twi in shaped_tweets:
        ml_date.append(twi["date"])
        ml_content.append(twi["content"])
        ml_impression.append(twi["impressions"])
        ml_retweet.append(twi["retweets"])
        ml_like.append(twi["likes"])
    
    """
    tweetsをDataframeにする処理も書く
    """

    traces = []
    traces.append(dict(
        x = ml_date,
        y = ml_impression,
        type = 'bar'
    ))

    return {
        'data': traces,
        'layout': dict(
            title = 'インプレッション数'
        )
    }

@app.callback(
    Output('tweet-list', 'children'),
    [Input('event-number','value')])
def update_table_event(event_number):
    tweets = session.query(Tweet.content,Tweet.date,Tweet.inpression,Tweet.retweet,Tweet.like).\
    filter(
        Tweet.date >= datetime(events_date[int(event_number)][0],events_date[int(event_number)][1],events_date[int(event_number)][2]),
        Tweet.date < datetime(events_date[int(event_number)][3],events_date[int(event_number)][4],events_date[int(event_number)][5]),
    ).\
    distinct(Tweet.date).all()

    shaped_tweets = shape_tweets_delta(tweets)

    ml_date = []
    ml_content = []
    ml_impression = []
    ml_retweet = []
    ml_like = []
    for twi in shaped_tweets:
        ml_date.append(twi["date"])
        ml_content.append(twi["content"])
        ml_impression.append(twi["impressions"])
        ml_retweet.append(twi["retweets"])
        ml_like.append(twi["likes"])
    
    tweet_df = pd.DataFrame({
        'date' : ml_date,
        'content' : ml_content,
        'impression' : ml_impression,
        'retweet' : ml_retweet,
        'like' : ml_like
    })

    return generate_table(tweet_df)

if __name__ == '__main__':
    app.run_server(debug=True)
