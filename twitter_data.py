"""
    File name: twitter_data.py
    Author: @hpandeycodeit
    Date created: 04/11/2020
    Tweepy Documentation: Ref: http://docs.tweepy.org/en/latest/getting_started.html

 """

import tweepy
import csv
import pandas as pd


# This code will not work without adding the following keys
consumer_key = '' # This needs to be added
consumer_secret = '' # This needs to be added
access_token = '' # This needs to be added
access_token_secret = '' # This needs to be added

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

class MyStreamListener(tweepy.StreamListener):


    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            try:
                
                tweet = status.retweeted_status.extended_tweet["full_text"]
                
            except:
                tweet = status.retweeted_status.text
        else:
            try: 
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text
        
        print (status.author.screen_name, status.created_at, tweet)
        with open('RealTime2.csv', 'a') as f: 
                    writer = csv.writer(f)
                    writer.writerow([status.author.screen_name, status.created_at,tweet])

        return True
 
    def on_error(self, status_code):
        print (sys.stderr, 'Error :', status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True 


with open('RealTime2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Date', 'Tweet'])

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode='extended')

# Hashtags specific to Election Day 2020 
myStream.filter(languages=["en"], track=['Elections2020', 'ElectionNight', 'Elections', 'Trump', 'Biden'])

 