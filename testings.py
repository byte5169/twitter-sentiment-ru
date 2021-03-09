# from dostoevsky.tokenization import RegexTokenizer
# from dostoevsky.models import FastTextSocialNetworkModel

# tokenizer = RegexTokenizer()
# tokens = tokenizer.split(
#     "всё очень плохо"
# )  # [('всё', None), ('очень', None), ('плохо', None)]

# model = FastTextSocialNetworkModel(tokenizer=tokenizer)

# messages = [
#     "привет",
#     "я люблю тебя!!",
#     "господи как же скучно вконтакте. что я здесь делаю?",
# ]

# results = model.predict(messages, k=2)

# for message, sentiment in zip(messages, results):
#     # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
#     # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
#     # малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
#     print(message, "->", sentiment)


import os
from numpy import kaiser
import tweepy
import pandas as pd
import re

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api")
api_secret = os.getenv("api_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

authenticate = tweepy.OAuthHandler(api_key, api_secret)
authenticate.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

import sys

dict1 = {}

name = "tutby"

# non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xFFFD)
# for full_tweets in tweepy.Cursor(
#     api.user_timeline, screen_name=name, timeout=999999
# ).items(3):
#     replies = []
#     for tweet in tweepy.Cursor(
#         api.search, q="to:" + name, result_type="recent", timeout=999999
#     ).items(1000):
#         if hasattr(tweet, "in_reply_to_status_id_str"):
#             if tweet.in_reply_to_status_id_str == full_tweets.id_str:
#                 replies.append(tweet.text)
#                 replies_copy = replies.copy()
#     print("Tweet :", full_tweets.text.translate(non_bmp_map))
#     dict1[full_tweets.text.translate(non_bmp_map)] = replies_copy
#     for elements in replies:
#         print("Replies :", elements)
#     replies.clear()
# print(dict1)


# from processing.data import get_tweet_replies

# a = get_tweet_replies("tutby", tweet_number=5)
# # df.to_csv('data/tweet_reply.csv', index=False)
# print(a)

# list1 = ["a", "b"]
# list2 = [1, 2, 3, 4]

# dict1 = {
#     'A' :
# }
# r = []
# c = []
# df = pd.DataFrame()
# for i in list1:
#     for b in list2:
#         r.append(i)
#         c.append(b)

# df["i"] = r
# df["k"] = c

# print(df)

# d = {}

# list1 = ["a", "b"]
# list2 = [1, 2, 3, 4]

# for i in list1:
#     for b in list2:
#         list3 = list2.copy()
#         d[i] = list3
#         list2.clear()

# print(d)

d = {
    "Как пойдет транспорт в Минске в понедельник, 8 марта?\n\nРассказываем. https://t.co/Vt5eA9JCRB https://t.co/dkLBEM5bAg": [
        "@tutby А главное куда..."
    ],
    "МВД сообщило о\xa0задержании брестских анархисты «из\xa0международной преступной организации».\n\nhttps://t.co/NMZmEt0CCV https://t.co/wIFBA0by60": [
        "@tutby что характерно, фамилии, на кого объявили розыск \n Александр Козлянко, Никита Дранец, Андрей Марач, Даниил Ч… https://t.co/JxNUAikkVM"
    ],
    "Что сейчас происходит вокруг «Беларуськалия» и\xa0Yara?\n\nСтачка\xa0— за\xa0разрыв договора, профсоюзы\xa0— против.… https://t.co/1WVsfvCdKe": [
        '@tutby Кого кроме разжигателей и фейкомётов из тутбай, может интересовать эта "срачка"? Которая, к тому же, в больш… https://t.co/BYvBAqOT2w',
        "@tutby The problem with sanctions is that it also ends up hurting the general public.\nThe chain reaction is complic… https://t.co/KJV5eMU2Ub",
        "@tutby А шахтеры знают, что их хотят лишить хорошей доли заработка?",
        "@tutby в любом случае выиграют россияне.",
        "@tutby стачком хочет уволить шахтеров, и их еще не закопали в шахте?",
        "@tutby Не чего не происходит, это вы так думаете что что-то там, Стачка это те упыри которые остались без работы и… https://t.co/VBkyHgTqP2",
    ],
}

df = pd.DataFrame([(k, *v) for k, v in d.items()])
df.columns = ["tweet"] + [f"reply{x}" for x in df.columns[1:]]
print(df)