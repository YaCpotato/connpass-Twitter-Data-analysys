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
from template.list_table import generate_table
from template.header import header
from utils.shape_tweets import by_day,by_tweet


external_stylesheets = ['style/myboard.css']

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
by_tweet_or_date = ['ツイート毎','日付毎']

app.layout = html.Div(
    children=[
        header(),
        html.Div(
            id='state-value',
            style={'display': 'none'},
            children=[]),
        html.Div(
            style={ 'width':'100vw',
                    'minHeight':'15vh',
                    'margin':'0 auto',
                    'textAlign':'center'
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
                    'textAlign':'left',
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
                dcc.Dropdown(
                    id='grain',
                    style={'width':'10vw','marginRight':'8px'},
                    options=[{'label': i, 'value': i} for i in by_tweet_or_date],
                    value=by_tweet_or_date[0]
                )
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
        )
    ]
)

@app.callback(
    Output('state-value','children'),
    [Input('subject','value'),Input('event-number','value'),Input('grain','value')])
def update_state_event(subject,event_number,grain):

    traces = []
    traces.append({
        'current_subject': subject,
        'current_event': event_number,
        'current_grain': grain
    })
    
    return {
        'data': traces
    }

@app.callback(
    [Output('graph-with-dropdown', 'figure'),Output('tweet-list', 'children')],
    [Input('state-value', 'children')])
def update_display_event(data):
    event_number = data['data'][0]['current_event']
    grain_size = data['data'][0]['current_grain']
    subject = data['data'][0]['current_subject']

    tweets = session.query(Tweet.content,Tweet.date,Tweet.inpression,Tweet.retweet,Tweet.like).\
    filter(
        Tweet.date >= datetime(events_date[int(event_number)][0],events_date[int(event_number)][1],events_date[int(event_number)][2]),
        Tweet.date < datetime(events_date[int(event_number)][3],events_date[int(event_number)][4],events_date[int(event_number)][5]),
    ).\
    distinct(Tweet.date).all()

    if grain_size == 'ツイート毎':
        shaped_tweets = by_tweet(tweets)
    elif grain_size == '日付毎':
        shaped_tweets = by_day(tweets)

    ml_date = []
    ml_content = []
    ml_subject = []
    ml_retweet = []
    ml_like = []
    ml_impression = []
    for twi in shaped_tweets:
        ml_date.append(twi["date"])
        ml_content.append(twi["content"])
        ml_impression.append(twi["impressions"])
        ml_retweet.append(twi["retweets"])
        ml_like.append(twi["likes"])
    
    if (subject == 'インプレッション数'):
        ml_subject = ml_impression
    elif (subject == 'RT数'):
        ml_subject = ml_retweet
    elif (subject == 'いいね数'):
        ml_subject = ml_like

    tweet_df = pd.DataFrame({
        'date' : ml_date,
        'content' : ml_content,
        'impression' : ml_impression,
        'retweet' : ml_retweet,
        'like' : ml_like
    })

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
    },generate_table(tweet_df)

if __name__ == '__main__':
    app.run_server(debug=True)
