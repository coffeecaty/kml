#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('dairy.db')
c = conn.cursor()
c.execute('''CREATE TABLE userlist(id INTEGER PRIMARY KEY,username TEXT,mute INTEGER);''')
c.close()

