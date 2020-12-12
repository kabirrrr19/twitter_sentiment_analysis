import streamlit as st
import warnings
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
from tweepy import Cursor
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
# EDA Pkgs
import pandas as pd
import numpy as np
import pandas as pd
import json
from tweepy import OAuthHandler
import re
import textblob
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import openpyxl
import time
import tqdm
import seaborn as sns

#To Hide Warnings
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

sns.set_style('darkgrid')







html_temp = """
<div style="background-color:black;"><p style="color:white;font-size:40px;padding:9px">Live twitter Sentiment analysis</p></div>
"""
st.markdown(html_temp, unsafe_allow_html=True)
st.subheader("Select a topic which you'd like to get the sentiment analysis on :")

tweets = []
################# Twitter API Connection #######################
consumerKey = 'TozjFECqWceNagY3yRfzNO96P'
consumerSecret = 'Inh4JKsasCmpkBSHPyW8JgFkRlZ0wRjXGwpdLUnlOXk4NEOrVa'
accessToken = '2467276230-2cAt3rrwIrKa5J930aL6RME9I9dzL5klPG87sES'
accessTokenSecret = 'HLdfqpXYvb9dq6bwu7PVNIeB45YXSF3AnoULkgU4CpgWm'
# Use the above credentials to authenticate the API.
auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)
################################################################


# Write a Function to extract tweets:
#tweets = tweepy.Cursor(api.search, q=searchTerm, lang="English").items(noOfSearchTerms)

searchTerm = st.text_input("Enter the Hashtag you wanna search")
noOfSearchTerms = st.text_input("Enter the Number of Search Terms")


def get_user_timeline_tweets(searchTerm, noOfSearchTerms):
    tweets = []
    for tweet in Cursor(self.twitter_client.user_timeline, id=searchTerm.twitter_user).items(noOfSearchTerms):
        tweets.append(tweet)
    return tweets


if searchTerm and noOfSearchTerms:
    tweets = api.user_timeline(screen_name=searchTerm, count=noOfSearchTerms)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    try :
        for tweet in tweets :
            print("tweets=", tweet.text)
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity
        
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity < 0.00):
                negative += 1
            elif (analysis.sentiment.polarity > 0.00):
                positive += 1
        def percentage(part, whole):
            return 100 * float(part)/float(whole)
        
        positive = percentage(positive, noOfSearchTerms)
        negative = percentage(negative, noOfSearchTerms)    
        neutral = percentage(neutral, noOfSearchTerms)

        positive = format(positive, '.2f')
        negative = format(negative, '.2f')
        neutral = format(neutral, '.2f')
        st.write("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " tweets.")
        if (polarity == 0):
            st.success('Neutral')
        elif (polarity < 0):
            st.success('Negative')
        elif (polarity > 0):
            st.success('Positive')
    except tweepy.error.TweepError :
            pass

    label = 'Positive [' + str(positive) + '%]','Neutral [' + str(neutral) + '%]', 'Negative[' + str(negative) + '%]'
    sizes = (positive, neutral, negative)
    colors = ['yellowgreen', 'gold', 'red']
    patches, texts = plt.pie(sizes, colors = colors, startangle = 90)
    plt.legend(patches, label, loc = "best")
    plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    explode = (0, 0, 0.1)
    plt.axis('equal')
    plt.tight_layout()
    st.pyplot()
else:
    st.text('Enter Your the hashtag and no. of tweets')


st.sidebar.info("A Twitter Sentiment analysis Project which will scrap twitter for the topic selected by the user. The extracted tweets will then be used to determine the Sentiments of those tweets. \
                The different Visualizations will help us get a feel of the overall mood of the people on Twitter regarding the topic we select.")


st.sidebar.header("For Any Queries/Suggestions Please reach out at :")
st.sidebar.info("kaustubhpandit24@gmail.com")
