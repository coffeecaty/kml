#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

def plog(update):
    print(update.message.from_user.username, ' ', update.message.from_user.id,
          ' ', str(update.message.date + timedelta(hours=8)))
    print(update.message.text)

def start(bot,update,args):
    plog(update)
    if args=[]:
        bot.sendMessage(update.message.from_user.id, text='欢迎使用小猫管家，本猫为私人管家，使用前请输入正确的使用密码。密码可以向我的主人 @coffeecaty 索取，当然他给不给你就不是我的问题了）')
    elif args[0]=config.psword:
        conn = sqlite3.connect('dairy.db')
        c = conn.cursor()
        tablename=str(update.message.from_user.id)
        c.execute(
            'CREATE TABLE ' +
            tablename +
            ' (id INTEGER PRIMARY KEY ,date TEXT,time TEXT,text TEXT);')
        conn.commit()
        conn.close()
        bot.sendMessage(update.message.from_user.id,
                        text='尊敬的'+update.message.from_user.username+',您已经通过验证，欢迎使用小猫管家系统，您可以使用/help查询具体的使用帮助，如有任何意见反馈，可以联系我的主人 @coffeecaty ，当然他给不给你改也就不是我的问题了）')
    else:
        bot.sendMessage(update.message.from_user.id,
                        text='您输入的使用密码不正确。正确密码可以向我的主人 @coffeecaty 索取，当然他给不给你依旧不是我的问题了噗）')

def main():

    # 导入config参数
    try:
        import config
    except ImportError:
        print('no config file')
        import sys
        sys.exit(0)
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # commands from base
    dp.add_handler(CommandHandler("start", base.start))


    # commands from talk
    dp.add_handler(MessageHandler([Filters.text], talk.talk))



    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
