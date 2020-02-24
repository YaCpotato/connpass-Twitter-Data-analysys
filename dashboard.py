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

# スペルミス等しないように定型文をdefineする
FormatDay = "%Y/%m/%d-"
FormatTime = "%H:%M:%S"

# 使いまわされそうなものは関数にする
def is_within_time(time,start,end):
    time = datetime.strftime(time,'%Y-%m-%d %H:%M')
    # FormatTimeだけだと年月が1990-1-1になるので現実の年月を使えるようにする
    date = datetime.strptime(time,'%Y-%m-%d %H:%M')
    start_time = datetime.strptime(start,'%Y-%m-%d %H:%M')
    end_time = datetime.strptime(end,'%Y-%m-%d %H:%M')
    return start_time < date < end_time

impressions = []
date = []
ml_impressions = []
ml_date = []
ml_retweet = []
ml_content = []
ml_like = []
tweets = session.query(Tweet).distinct(Tweet.date).all()

for tweet in tweets:
    if '#MLbeginners' in tweet.content and is_within_time(tweet.date,'2019-10-02 00:00','2019-10-27 13:00'):
            ml_content.append(tweet.content)
            ml_date.append(tweet.date)
            ml_impressions.append(tweet.inpression)
            ml_retweet.append(tweet.retweet)
            ml_like.append(tweet.like)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children=[
        html.Div(style={'max-height':'50vh','overflow-y':'scroll'},children=[
            str(len(tweets))+'のうち、'+str(len(ml_impressions))+'件が#MLbeginners関連のツイートでした',
                generate_table(pd.DataFrame({
                                                'content' : ml_content,
                                                'date' : ml_date,
                                                'impression' : ml_impressions,
                                                'retweet' : ml_retweet,
                                                'like' : ml_like
                                            })
                )
        ]
    ),
    html.Div(children=[
    dcc.Graph(
        id='example-graph-1',
        figure={
            'data': [
                {'x': ml_date, 'y': ml_impressions, 'type': 'bar', 'name': 'SF'},
            ],
            'layout': {
                'title': 'インプレッション数'
            }
        }
    ),
    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': ml_date, 'y': ml_retweet, 'type': 'line', 'name': 'SF'},
            ],
            'layout': {
                'title': 'リツイート数'
            }
        }
    ),
    dcc.Graph(
        id='example-graph-3',
        figure={
            'data': [
                {'x': ml_date, 'y': ml_like, 'type': 'line', 'name': 'SF'},
            ],
            'layout': {
                'title': 'いいね数'
            }
        }
    )
    ])
])])


if __name__ == '__main__':
    app.run_server(debug=True)
