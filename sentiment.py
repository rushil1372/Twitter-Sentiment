# Tweepy 3.10.0

import os
from dotenv import load_dotenv

import tweepy as tw
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np


import streamlit as st 

from textblob import TextBlob
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

# Authentication 

load_dotenv('.env')

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

# def printenvironment():
#     print(f'The client id is: {consumer_key}.')
#     print(f'The secret id is: {consumer_secret}.')
#     print(f'The access token is: {access_token}.')
#     print(f'The access secret token is: {access_token_secret}.')
# printenvironment()

# Tweepy supports both OAuth 1a (application-user) and OAuth 2 (application-only) authentication.
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) # use smaller batches during api calls  

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Input GUI
from inputGUI import *

tweets = tw.Cursor(api.search, q="%s" %keyword, lang="en",since=start_date, tweet_mode='extended').items(ntweets) #from:user #-filter:retweets

# Front-end 

# st.title("Twitter Sentiment Analysis")
# st.markdown("The dashboard analyzes tweets based on user input and shows polarity of the tweet.")


# Preprocessed 
    
def percentage(part, whole):
    return 100 * float(part)/float(whole)

positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

for tweet in tweets:
    #print("-------------------")
    #print(tweet.full_text)
    #print("-------------------")
    tweet_list.append(tweet.full_text)
    analysis = TextBlob(tweet.full_text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.full_text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if neg > pos:
        negative_list.append(tweet.full_text)
        negative += 1
        
    elif pos > neg:
        positive_list.append(tweet.full_text)
        positive += 1
 
    elif pos == neg:
        neutral_list.append(tweet.full_text)
        neutral += 1
        
positive = percentage(positive, ntweets)
negative = percentage(negative, ntweets)
neutral = percentage(neutral, ntweets)
polarity = percentage(polarity, ntweets)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

print("Positive : " + positive + " %" + " includes " + str(len(positive_list)))
print("Negative : " + negative + " %" + " includes " + str(len(negative_list)))
print("Neutral : " + neutral + " %" + " includes " + str(len(neutral_list)))
# print(polarity)

tw_list = pd.DataFrame(tweet_list)
tw_list["text"] = tw_list[0]

# Data Cleaning 
# Removing RT, Punctuation 

remove_rt = lambda x: re.sub(r'RT @\w+: '," " ,x)
rt = lambda x: re.sub(r'[^\w\s]', '', x)
nl = lambda x: re.sub(r'[\n]',' ',x)
tw_list["text"] = tw_list.text.map(remove_rt)
tw_list["text"] = tw_list.text.map(rt)
tw_list["text"] = tw_list.text.map(nl) 
tw_list["text"] = tw_list.text.str.lower()
tw_list["text"] = tw_list.text.str.strip()
# print(tw_list.head(10))
# print(tw_list['text'])


positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

print("-------------------")
for twInL in tw_list["text"]:
    #print("-------------------")
    #print(tweet.full_text)
    #print("-------------------")
    tweet_list.append(twInL)
    analysis = TextBlob(twInL)
    score = SentimentIntensityAnalyzer().polarity_scores(twInL)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if neg > pos:
        negative_list.append(twInL)
        negative += 1
        
    elif pos > neg:
        positive_list.append(twInL)
        positive += 1
 
    elif pos == neg:
        neutral_list.append(twInL)
        neutral += 1
        
positive = percentage(positive, ntweets)
negative = percentage(negative, ntweets)
neutral = percentage(neutral, ntweets)
polarity = percentage(polarity, ntweets)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

print("Positive : " + positive + " %" + " includes " + str(len(positive_list)))
print("Negative : " + negative + " %" + " includes " + str(len(negative_list)))
print("Neutral : " + neutral + " %" + " includes " + str(len(neutral_list)))

# # Processing GUI
# from prepostGUI import *

# Pie Chart
labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90,explode = (0.01, 0.01, 0.01))
plt.style.use('default')
plt.legend(labels)
plt.title("Sentiment Analysis Result for keyword= "+keyword+"" )
plt.axis('equal')
plt.show()

# Bar Chart 
# Sentiment = ['Positive','Neutral','Negative']
# notweets = [positive,neutral,negative]
# plt.bar(Sentiment, notweets)
# plt.title('Sentiment Vs %. of tweets')
# plt.xlabel('Sentiment')
# plt.ylabel('No. of tweets')
# plt.show()

# notweets = [positive, neutral, negative]
# bars = ('Positive', 'Neutral', 'Negative')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, notweets, color=(0.2, 0.4, 0.6, 0.6))
# plt.xlabel('%. of tweets v/s sentiment', fontweight='bold', color = 'orange', fontsize='17', horizontalalignment='center')
# plt.show()