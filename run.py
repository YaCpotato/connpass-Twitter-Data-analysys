# -*- coding:utf-8 -*-
import json, config
from requests_oauthlib import OAuth1Session

def searchWords():
	url = "https://api.twitter.com/1.1/search/tweets.json"
	print("何を調べますか?")
	keyword = input('>> ')
	print('----------------------------------------------------')
	params = {'q' : keyword, 'count' : 5}
	req = twitter.get(url, params = params)

	if req.status_code == 200:
		search_timeline = json.loads(req.text)
		for tweet in search_timeline['statuses']:
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
	searchWords()
