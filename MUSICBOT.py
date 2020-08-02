#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!,ENTER ANY SONG NAME WHICH YOU WILL LIKE TO DOWNLOAD!!!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('USE /list FOR LIST OF COMMANDS')


def donate(update, context):
    update.message.reply_text('THANKS FOR HITTING DONATE, FOR NOW THERE IS NO OPTION FOR DONATE.')


def echo(update, context):
    """Echo the user message."""
    # update.message.reply_text(update.message.text)


def song(update, context):
    class Processing:
        def __init__(self, albumname, songname, singername, downloadlink):
            self.album = albumname
            self.name = songname
            self.singer = singername
            self.link = downloadlink

        def results(self):
            return f"SONG:{self.name}\nALBUM: {self.album}\nSINGER: {self.singer}\n THE DOWNLOAD LINK TO ABOVE SONG IS:{self.link}"

    search = update.message.text
    url = "API"
    r = requests.get(url + search)
    answer = r.text
    jsondata = json.loads(answer)
    empty_list = []
    for item in jsondata:
        object = Processing(item["album"], item["song"], item["singers"], item["media_url"])
        empty_list.append(object)

def lists(update, context):
    update.message.reply_text(["/start", "/help", "/donate"])


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("Token", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("list", lists))
    dp.add_handler(CommandHandler("donate", donate))

    # on noncommand i.e message - echo the message on Telegram

    dp.add_handler(MessageHandler(Filters.text, song))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
