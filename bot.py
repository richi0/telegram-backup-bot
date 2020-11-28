import logging
import pprint
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
        start_string = ("/help {command}\n"
                        "/login {password}\n"
                        "/search {query}\n"
                        "/get {file_id}\n"
                        "/start\n\n"
                        "Send data to me and I will store it for you")
        self.answer(start_string)


class Help(Command):
    def __init__(self, update, context):
        super().__init__(update, context)
        self.check_args()
        if self.check:
            arg = self.arg.lower()
            if "start" in arg:
                self.answer(("Start command:\n"
                             "The start command returns all available commands "
                             "it has no arguments."
                             ))
            if "login" in arg:
                self.answer(("Login command:\n"
                             "You have to send a password with the login command. "
                             "If the password is correct you get a success message. "
                             "Else you get a wrong password message.\n\n"
                             "Example: /login 9876\n\n"
                             "Once you are logged in successfully "
                             "your account will be saved "
                             "as authorized and you never have to login again. "
                             "You need to be logged in to send data, search data or get data."
                             ))
            elif "search" in arg:
                self.answer(("Search command:\n"))
            elif "get" in arg:
                self.answer(("Get command:\n"
                             "You have to send a file id or a list of file ids "
                             "with the get command. To get a file id use the search "
                             "command. \n\n"
                             "Example 1: /get 123456\n"
                             "The bot will send you the file 123456\n\n"
                             "Example 2: /get [123456, 987654]\n"
                             "The bot will send you the files 123456 and 987654\n\n"
                             "You need to be logged in to use the get command."
                             ))
            else:
                self.answer(("Use one of the following arguments: "
                             "start, login, search, get."
                             "\n\n Or send a file to store it."))


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
                self.answer("Wrong password")


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
        if self.request.user.authorized:
            message = self.update.message
            if message.photo:
                photo = message.photo[-1]
                file_id = photo.file_id
                file_type = "photo"
            elif message.video:
                file_id = message.video.file_id
                file_type = "video"
            elif message.audio:
                file_id = message.audio.file_id
                file_type = "audio"
            elif message.document:
                file_id = message.document.file_id
                file_type = "document"
            with io.BytesIO() as fp:
                file_info = self.context.bot.get_file(file_id)
                if message.document:
                    name = message.document.file_name
                elif message.audio:
                    name = message.audio.title + \
                        Path(file_info.file_path).suffix
                else:
                    name = Path(file_info.file_path).name
                file_info.download(out=fp)
                info = {"file_name": name,
                        "file_type": file_type,
                        "extension": Path(name).suffix,
                        "size": file_info.file_size}
                self.request.add_file(info, fp)
            self.answer(f"Your file ({info['file_name']}) was saved")
        else:
            self.answer(
                "You have to login to upload files \n/login {password}")


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

    filters = [Filters.photo, Filters.video, Filters.audio, Filters.document]
    for filter in filters:
        handler = MessageHandler(filter, Doc)
        dispatcher.add_handler(handler)

    logger.warning("Bot is listening...")
    updater.start_polling()
