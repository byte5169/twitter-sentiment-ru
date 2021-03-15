from pandas.core.frame import DataFrame
from processing.data import get_tweets, load_clean_data_to_df, get_tweet_replies
from processing.sentiment import sentiment_all_tweets, get_sentiment_list
from processing.visualize import word_cloud_image
import pandas as pd

from processing.data import clean_txt


def main():
    get_tweets("tutby", 200, "ru").to_csv(
        "data/tweets_tutby.csv", index=False, mode="w+"
    )

    df = pd.DataFrame(load_clean_data_to_df("data/tweets_tutby.csv"))

    word_cloud_image(df, "Tweets", "data/tutby_wordcloud.png")

    sentiment_all_tweets(df, "Tweets").to_csv(
        "data/tutby_200tweets.csv", index=False, mode="w+"
    )

    get_tweet_replies("tutby", tweet_count=200).to_csv(
        "data/tutby_replies.csv", index=False, mode="w+"
    )

    load_clean_data_to_df("data/tutby_replies.csv").to_csv(
        "data/tutby_replies_clean.csv", index=False, mode="w+"
    )


if __name__ == "__main__":
    main()
