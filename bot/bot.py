"""
Relative imports (as in from .. import mymodule) only work in a package.
To import 'mymodule' that is in the parent directory of your current module with use the code below
"""
import os, sys, inspect

from six import text_type

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import logging
import telebot
import pandas as pd

from processing.sentiment import get_sentiment_string
from processing.data import get_tweets, clean_txt
from dotenv import load_dotenv

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
load_dotenv()
bot_token = os.getenv("bot_token")
bot = telebot.TeleBot(bot_token, parse_mode=None)


"""
Handling start of the bot
"""
commands = {
    "help": "Gives you information about the available commands",
    "sentiment": "Gives you 10 latest tweets analyzed from user",
}


@bot.message_handler(commands=["start"])
def command_start(m):
    cid = m.chat.id
    bot.send_message(
        cid,
        "Hello! \nType /help for all available commands.",
    )


@bot.message_handler(commands=["help"])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


"""
Handling tweets sentiment
"""
name = ""
number_tweets = 5


@bot.message_handler(content_types=["text"])
def twitter_sentiment(m):
    cid = m.chat.id
    if m.text == "/tweets":
        bot.send_message(cid, "Please enter twitter account name.")
        bot.register_next_step_handler(m, handle_tweet_count)
    else:
        bot.send_message(cid, "Please type /tweets")


def handle_tweet_count(m):
    global name
    name = m.text
    cid = m.chat.id
    bot.send_message(cid, "Please enter number of tweets you want to see.")
    bot.register_next_step_handler(m, handle_twitter_info)


def handle_twitter_info(m):
    global number_tweets
    number_tweets = m.text
    cid = m.chat.id
    try:
        df = get_tweets(name, tweet_count=number_tweets, lang="ru")
        all_tweets = df["Tweets"].to_list()

        for tweet in all_tweets:
            clean_tweet = clean_txt(tweet)
            sentiment_tweet = get_sentiment_string(clean_tweet)
            for sentiment in sentiment_tweet:
                bot.send_message(cid, f"{clean_tweet} \n Results: \n {sentiment}")

    except Exception:
        bot.send_message(cid, "Account doesn't exist, please enter the correct one.")
        bot.register_next_step_handler(m, handle_tweet_count)


bot.polling()


### FEATURES
# limit latest number of tweets
# clean up sentiment output
# decide how to choose a tweet for analyze
# add sentiment for random text

### BUGS
# currently there is a bug, you need to enter correct number twice