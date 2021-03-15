import os
from matplotlib.pyplot import axis
import tweepy
import pandas as pd
import re
import sys

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api")
api_secret = os.getenv("api_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")


def get_tweets(screen_name, tweet_count=100, lang="en", tweet_mode="extended"):
    """
    saves twitter posts in a CSV file

    :screen_name: twitter account name \n
    :tweet_count: number of tweets to load \n
    :lang: tweet language \n
    :tweet_mode: tweet mode \n
    :return: a dataframe
    """
    authenticate = tweepy.OAuthHandler(api_key, api_secret)
    authenticate.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    posts = api.user_timeline(
        screen_name=screen_name, count=tweet_count, lang=lang, tweet_mode=tweet_mode
    )

    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=["Tweets"])

    return df


def get_tweet_replies(
    screen_name,
    tweet_count=10,
):
    """
    gets twitter replies to df

    :screen_name: twitter account name \n
    :tweet_count: number of tweets to load \n
    :return: a dataframe
    """

    authenticate = tweepy.OAuthHandler(api_key, api_secret)
    authenticate.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    name = screen_name
    d = {}

    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xFFFD)
    for full_tweets in tweepy.Cursor(
        api.user_timeline, screen_name=name, timeout=999999
    ).items(tweet_count):
        replies = []
        for tweet in tweepy.Cursor(
            api.search, q="to:" + name, result_type="recent", timeout=999999
        ).items(1000):
            if hasattr(tweet, "in_reply_to_status_id_str"):
                if tweet.in_reply_to_status_id_str == full_tweets.id_str:
                    replies.append(tweet.text)
                    replies_copy = replies.copy()
        print("Tweet :", full_tweets.text.translate(non_bmp_map))
        d[full_tweets.text.translate(non_bmp_map)] = replies_copy
        for elements in replies:
            print("Replies :", elements)
        replies.clear()

    df = pd.DataFrame([(k, *v) for k, v in d.items()])
    df.columns = ["tweet"] + [f"reply{x}" for x in df.columns[1:]]

    return df


def clean_txt(text):
    """
    regex data cleaning out of hash tags, mentions, urls

    :return: cleaned input as a string
    """
    text = re.sub("@[A-Za-z0–9]+", "", text)  # Removing @mentions
    text = re.sub("#", "", text)  # Removing '#' hash tag
    text = re.sub("RT[\s]+", "", text)  # Removing RT
    text = re.sub("https?:\/\/\S+", "", text)  # Removing hyperlink

    return text


def load_clean_data_to_df(csv_path):
    """
    takes raw CSV with data \n
    replace empty rows with NaN \n
    loads cleaned strings from all columns to dataframe

    :csv_path: path to CSV with raw data \n
    :return: a dataframe
    """
    df = pd.read_csv(csv_path)
    df = df.fillna("NaN")
    for column in df:
        df[column] = df[column].apply(clean_txt)

    return df
