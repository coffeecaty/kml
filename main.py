#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
from plog import plog
from decorator import al
from datetime import timedelta
import config,sqlite3

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot,update,args):
    plog(update)
    if args==[]:
        bot.sendMessage(update.message.from_user.id, text='欢迎使用小猫管家，本猫为私人管家，使用前请输入正确的使用密码。密码可以向我的主人 @coffeecaty 索取，当然他给不给你就不是我的问题了喵）')
    elif args[0]==config.psword:
       try:
        conn = sqlite3.connect('dairy.db')
        c = conn.cursor()
        c.execute('insert into userlist VALUES (?,?,0);',(update.message.from_user.id,update.message.from_user.username))
        conn.commit()
        tablename='dairy'+str(update.message.from_user.id)
        c.execute(
            'CREATE TABLE ' +
            tablename +
            ' (id INTEGER PRIMARY KEY ,date TEXT,time TEXT,text TEXT);')
        conn.commit()
        conn.close()
        bot.sendMessage(update.message.from_user.id,
                        text='尊敬的'+update.message.from_user.username+',您已经通过验证，欢迎使用小猫管家系统，您可以使用/help查询具体的使用帮助，如有任何意见反馈，可以联系我的主人 @coffeecaty ，当然他给不给你改也就不是我的问题了喵）')
       except (sqlite3.OperationalError,sqlite3.IntegrityError):
           bot.sendMessage(update.message.from_user.id,
                           text='尊敬的' + update.message.from_user.username + ',您早已经通过验证了哦？不必重复验证喵（')
    else:
        bot.sendMessage(update.message.from_user.id,
                        text='您输入的使用密码不正确。正确密码可以向我的主人 @coffeecaty 索取，当然他给不给你依旧不是我的问题了噗）')

@al()
def record(bot,update):
    plog(update)
    conn = sqlite3.connect('dairy.db')
    c = conn.cursor()
    tablename = 'dairy' + str(update.message.from_user.id)
    datetime=update.message.date + timedelta(hours=8)
    date=str(datetime.date())
    time=str(datetime.time())
    text=update.message.text
    c.execute('insert into '+tablename+'(date,time,text) VALUES (?,?,?);', (date,time,text))
    conn.commit()
    c.execute('SELECT mute from userlist where id=?;',(update.message.from_user.id,))
    if not c.fetchall()[0][0]:
        bot.sendMessage(update.message.from_user.id,
                        text='recording')
    c.close()

@al()
def list(bot,update,args=[]):
    plog(update)
    if args==[]:
        date=update.message.date+timedelta(hours=-16)
        date=str(date.date())
    elif len(args[0])!=8:
        bot.sendMessage(update.message.from_user.id,
                        text='请输入正确的8位时间格式查询日记喵（')
        return
    else:
        date=args[0][:4]+"-"+args[0][4:6]+"-"+args[0][-2:]
    tablename = 'dairy' + str(update.message.from_user.id)
    conn = sqlite3.connect('dairy.db')
    c = conn.cursor()
    c.execute('SELECT time,text from '+tablename+' where date=?;',(date,))
    result = c.fetchall()
    c.close()
    if result:
        text="日记时间 "+date
        for n in result:
            text=text+'\n'+n[0]+' '+n[1]
        bot.sendMessage(update.message.from_user.id,
                        text=text)
    else:
        bot.sendMessage(update.message.from_user.id,
                        text='未找到您当天的记录喵（')

@al()
def mute(bot,update):
    plog(update)
    conn = sqlite3.connect('dairy.db')
    c = conn.cursor()
    c.execute('SELECT mute from userlist where id=?;', (update.message.from_user.id,))
    mute=c.fetchall()[0][0]
    mute=-abs(mute)+1
    c.execute('update userlist set mute=? WHERE id=?;',(mute,update.message.from_user.id,))
    conn.commit()
    c.close()
    if mute:
        bot.sendMessage(update.message.from_user.id,
                        text='已屏蔽记录反馈信息')
    else:
        bot.sendMessage(update.message.from_user.id,
                        text='已解除记录反馈信息的屏蔽')

@al()
def help(bot,update):
    plog(update)
    text='''直接输入文字即可记录日记
    /list 时间，显示某天的全部记录，时间格式为8位，如20180630，不填时间默认显示昨天的记录
    /mute 屏蔽/开启记录日记后的recording反馈，默认为开启状态
    有任何意见可联系主人 @coffeecaty 但他不会理你们的喵哈哈哈哈'''
    bot.sendMessage(update.message.from_user.id,
                    text=text)




def main():
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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
    dp.add_handler(CommandHandler("start", start,pass_args=True))
    dp.add_handler(MessageHandler([Filters.text], record))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("h", help))
    dp.add_handler(CommandHandler("list", list,pass_args=True))
    dp.add_handler(CommandHandler("l", list,pass_args=True))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("m", mute))



    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
