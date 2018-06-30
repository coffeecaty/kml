#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import main
from decorator import al


class update:
    pass


class message:
    def reply_text(self, date):
        print(date)


class from_user:
    pass


class bot:
    def sendMessage(self, x, *, text):
        print('send message to ', x, ' : ', text)


from datetime import datetime,timedelta


from_user.username = 'test'
from_user.id=1895
message.from_user = from_user()
message.chat_id = 1895
update.message = message()
message.date = datetime.now()+timedelta(days=1)
message.text = 'text test5'
t = update()

#main.start(bot(),t,['psw'])
#main.record(bot(),t)
main.list(bot(),t,[])

