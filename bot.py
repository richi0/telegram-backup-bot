import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from settings import token, password, db_logging
from models import User, Base
from middleware import Request

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    level=logging.DEBUG)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def login(update, context):
    request = Request(update)
    submitted_pw = update.message.text.split(" ")[1]
    if submitted_pw == password:
        request.authorize_user()
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Login successful")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Login unsuccessful")


def start(update, context):
    print(update.message.text)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    request = Request(update)
    print(request.user.authorized)
    print()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == "__main__":
    engine = create_engine('sqlite:///data.db', echo=db_logging)
    Base.metadata.create_all(engine)

    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    ed_user = User(name='ed', telegram_id="12345678999")
    session.add(ed_user)

    session.commit()
    our_user = session.query(User).all()
    for i in our_user:
        print(i)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    login_handler = CommandHandler('login', login)
    dispatcher.add_handler(login_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
