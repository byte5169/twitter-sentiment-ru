"""
Relative imports (as in from .. import mymodule) only work in a package.
To import 'mymodule' that is in the parent directory of your current module with use the code below
"""
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from processing.sentiment import get_sentiment_string
from processing.data import get_tweets, clean_txt


"""
Credentials
"""
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("bot_token")

"""
Logging
"""
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

"""
Handling unknown commands
"""


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


"""
Start command
"""


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""Type /text followed by a text to get sentiment for that line. \nExample "/text Привет ублюдок!" \nType /tweets followed by a twitter profile name to get sentiment for the latest 10 tweets. \nExample "/tweets tutby". \nNB! Works only for RU accounts and RU language. """,
    )


"""
text_sentiment_handler
"""


def text_sentiment(update, context):
    line = " ".join(context.args)
    sentiment_line = get_sentiment_string(line)
    text = f"Original: \n {line} \n Results: \n {sentiment_line}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


"""
twitter_sentiment_handler
Sentiment for the latest 10 tweets of the given account name 
"""


def tweet_sentiment(update, context):
    screen_name = (context.args)[0]
    tweets = get_tweets(screen_name=screen_name, tweet_count=10, lang="ru")
    tweet_list = tweets["Tweets"].tolist()
    for t in tweet_list:
        clean_t = clean_txt(t)
        sentiment_tweet = get_sentiment_string(clean_t)
        text = (
            f"Original tweet: \n \n {t} \n \n Sentiment results: \n {sentiment_tweet}"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


"""
Main function
"""


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("text", text_sentiment))
    dispatcher.add_handler(CommandHandler("tweets", tweet_sentiment))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Bot start/stop
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()


# https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples