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

def shape_tweets_by_tweet(tweets):
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

def shape_tweets_by_day(tweets):
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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
events_number = [0,1,2,3]
events_date = [
    [2019,10,2,2019,10,28],
    [2019,11,8,2019,12,5],
    [2019,12,14,2020,1,19],
    [2020,1,27,2020,2,27]
]
subject = ['インプレッション数','RT数','いいね数']

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
    [Input('subject','value'),Input('event-number','value')])
def update_display_event(subject,event_number):
    tweets = session.query(Tweet.content,Tweet.date,Tweet.inpression,Tweet.retweet,Tweet.like).\
    filter(
        Tweet.date >= datetime(events_date[int(event_number)][0],events_date[int(event_number)][1],events_date[int(event_number)][2]),
        Tweet.date < datetime(events_date[int(event_number)][3],events_date[int(event_number)][4],events_date[int(event_number)][5]),
    ).\
    distinct(Tweet.date).all()

    shaped_tweets = shape_tweets_by_day(tweets)

    ml_date = []
    ml_content = []
    ml_subject = []
    for twi in shaped_tweets:
        ml_date.append(twi["date"])
        ml_content.append(twi["content"])
        if (subject == 'インプレッション数'):
            ml_subject.append(twi["impressions"])
        elif (subject == 'RT数'):
            ml_subject.append(twi["retweets"])
        elif (subject == 'いいね数'):
            ml_subject.append(twi["likes"])
    
    """
    tweetsをDataframeにする処理も書く
    """

    traces = []
    traces.append(dict(
        x = ml_date,
        y = ml_subject,
        type = 'bar'
    ))

    return {
        'data': traces,
        'layout': dict(
            title = subject
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

    shaped_tweets = shape_tweets_by_day(tweets)

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
