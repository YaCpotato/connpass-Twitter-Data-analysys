# -*- coding:utf-8 -*-
import json, config
from requests_oauthlib import OAuth1Session

def myTimeLine():
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	params ={'count' : 20}
	req = twitter.get(url, params = params)
	if req.status_code == 200:
		timeline = json.loads(req.text)
		for tweet in timeline:
			print(tweet['user']['name']+'::'+tweet['text'])
			print(tweet['created_at'])
			print('----------------------------------------------------')
	else:
		print("ERROR: %d" % req.status_code)
		
	return

def myTimeLineTweetsId():
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params ={'count' : 20}
    req = twitter.get(url, params = params)
    ids = []
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            ids.append(tweet['id'])
    else:
        print("ERROR: %d" % req.status_code)
 
    return ids

def getInpressions():
    url = "https://data-api.twitter.com/insights/engagement/totals"
    params = { 'tweet_ids':["1230059041730154497"],"engagement_types": ["impressions","engagements","favorites"],\
    "groupings": {"grouping name": {"group_by": ["tweet.id"]}}}
    req = twitter.post(url, params = params)
    print(vars(req))
    if req.status_code == 200:
        print('success')
    else:
        print(req.status_code)
    return

def searchWords():
	#url = "https://api.twitter.com/1.1/search/tweets.json"
	url = "https://api.twitter.com/1.1/tweets/search/30day/MyPortfolio.json"
	print("何を調べますか?")
	keyword = input('>> ')
	print('----------------------------------------------------')
	params = {'query' : keyword, 'maxResults' : 10,'fromDate':'202002010000','toDate':'202002100000'}
	req = twitter.get(url, params = params)

	if req.status_code == 200:
		search_timeline = json.loads(req.text)
		print(len(search_timeline['results']))
		for tweet in search_timeline['results']:
			print(tweet['user']['name'] + '::' + tweet['text'])
			print(tweet['created_at'])
			print('----------------------------------------------------')
		return;
	else:
		print("ERROR: %d" % req.status_code)
	return;

if __name__ == '__main__':
    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS)
    #searchWords()
    #myTimeLineTweetsId()
    getInpressions()
