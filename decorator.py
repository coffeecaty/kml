import sqlite3

def al():
    def decorator(func):
        def wrapper(*args, **kw):
            conn = sqlite3.connect('dairy.db')
            c = conn.cursor()
            id=args[1].message.from_user.id
            c.execute('SELECT id FROM userlist WHERE id=?', (id,))
            if c.fetchall():
                c.close()
                return func(*args,**kw)
            else:
                c.close()
                return args[0].sendMessage(args[1].message.from_user.id,
                        text='您没有获得本猫的使用权限，请使用/start获得权限后使用相关功能')
                return
        return wrapper

    return decorator