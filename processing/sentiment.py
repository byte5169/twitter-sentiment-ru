from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import pandas as pd

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def get_sentiment_string(text):
    """
    :return: sentiment for a single string
    """
    results = model.predict([text], k=2)
    return results


def get_sentiment_list(text_list):
    """
    :return: sentiments for a list
    """
    results = model.predict(text_list, k=2)
    return results


def sentiment_all_tweets(df, column_for_sentiment):
    """
    :return: a dataframe with columns:
    text, neutral, negative, positive
    """
    tweet_list = df[column_for_sentiment].tolist()

    df_text = pd.DataFrame()
    df_text["text"] = tweet_list

    sentiment_list = []
    results = get_sentiment_list(tweet_list)
    for sentiment in results:
        sentiment_list.append(sentiment)

    neutral_list = []
    negative_list = []
    positive_list = []

    for sentiment in sentiment_list:
        neutral = sentiment.get("neutral")
        negative = sentiment.get("negative")
        positive = sentiment.get("positive")
        if neutral is None:
            neutral_list.append(0)
        else:
            neutral_list.append(sentiment.get("neutral"))
        if negative is None:
            negative_list.append(0)
        else:
            negative_list.append(sentiment.get("negative"))
        if positive is None:
            positive_list.append(0)
        else:
            positive_list.append(sentiment.get("positive"))
    df_text["negative"] = negative_list
    df_text["positive"] = positive_list
    df_text["neutral"] = neutral_list

    return df_text
