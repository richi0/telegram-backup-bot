import logging
import io

from pathlib import Path

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import File

from settings import token, password
from commands import Command

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    level=logging.WARNING)

logger = logging.getLogger('debug_print')


class Start(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        start_string = "\n".join(["/help {command}", "/login {password}", "/search {query}",
                                  "/get {file_id}", "/start", "", "Send data to me and I will store it for you"])
        self.answer(start_string)


class Help(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        self.check_args()
        if self.check:
            self.answer("Help")


class Login(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        self.check_args()
        if self.check:
            submitted_pw = self.arg
            if submitted_pw == password:
                self.request.authorize_user()
                self.answer("Login successful")
            else:
                self.answer("Login unsuccessful")


class Search(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        self.check_args()
        if self.check:
            self.answer("Search")


class Get(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        self.check_args()
        if self.check:
            self.answer("Get")


class Doc(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        with io.BytesIO() as fp:
            name = self.update.message.document.file_name
            file_id = self.update.message.document.file_id
            file_info = self.context.bot.get_file(file_id)
            file_info.download(out=fp)
            info = {"file_name": name,
                    "extension": Path(name).suffix,
                    "size": file_info.file_size}
            self.request.add_file(info, fp)
        self.answer("Your message contained a document")


if __name__ == "__main__":
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', Start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', Help)
    dispatcher.add_handler(help_handler)

    login_handler = CommandHandler('login', Login)
    dispatcher.add_handler(login_handler)

    search_handler = CommandHandler('search', Search)
    dispatcher.add_handler(search_handler)

    get_handler = CommandHandler('get', Get)
    dispatcher.add_handler(get_handler)

    filters = [Filters.photo, Filters.video, Filters.document]
    for filter in filters:
        handler = MessageHandler(filter, Doc)
        dispatcher.add_handler(handler)

    logger.warning("Bot is listening...")
    updater.start_polling()
