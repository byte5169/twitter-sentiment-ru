from processing.data import get_twitter_data, load_clean_data_to_df
from processing.sentiment import sentiment_all_tweets
from processing.visualize import word_cloud_image
import pandas as pd


def main():
    # get_twitter_data("tutby", 200, "ru", csv_path="data/tweets_tutby.csv")

    df = pd.DataFrame(load_clean_data_to_df("data/tweets_tutby.csv"))

    word_cloud_image(df, "Tweets", "data/tutby_wordcloud.png")

    sentiment_all_tweets(df, "Tweets").to_csv("data/tutby_200tweets.csv")


if __name__ == "__main__":
    main()

# df = pd.DataFrame(load_clean_data_to_df("data/tweets_tutby.csv"))
# df = sentiment_all_tweets(df, "Tweets")
# df["is_negative"] = df["negative"].apply(lambda i: True if 0.1 <= i else False)
# df["is_positive"] = df["positive"].apply(lambda i: True if 0.1 <= i else False)
# df = df.sort_values(by="positive", ascending=False)
# print(df.head(50))