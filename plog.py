from datetime import timedelta

def plog(update):
    print(update.message.from_user.username, ' ', update.message.from_user.id,
          ' ', str(update.message.date + timedelta(hours=8)))
    if update.message.text[0]=="/":
        print(update.message.text)
    else:
        print("recording something")