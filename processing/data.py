import os
import tweepy
import pandas as pd
import re

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api")
api_secret = os.getenv("api_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")


def get_twitter_data(
    screen_name, tweet_count=100, lang="en", tweet_mode="extended", csv_path="temp.csv"
):
    """
    saves twitter posts in a CSV file

    :screen_name: twitter account name \n
    :tweet_count: number of tweets to load \n
    :lang: tweet language \n
    :tweet_mode: tweet mode \n
    :csv_path: path to save CSV file
    """
    authenticate = tweepy.OAuthHandler(api_key, api_secret)
    authenticate.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    posts = api.user_timeline(
        screen_name=screen_name, count=tweet_count, lang=lang, tweet_mode=tweet_mode
    )

    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=["Tweets"])

    df.to_csv(csv_path, mode="w+", index=False)


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


def load_clean_data_to_df(csv_path, column_name="Tweets"):
    """
    takes raw CSV with data (tweets)
    loads cleaned strings to dataframe

    :csv_path: path to CSV with raw data \n
    :column_name: columns name where clean data will be stored \n
    :return: a dataframe
    """
    df = pd.read_csv(csv_path)
    df[column_name] = df[column_name].apply(clean_txt)

    return df
