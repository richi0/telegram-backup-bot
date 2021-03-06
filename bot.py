"""This module starts a telegram bot that can backup and return document, video, photo and audio data."""

import logging
import pprint
import io
import datetime
from pathlib import Path

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, File, Message, Chat

from settings import telegram_api_token, bot_access_password
from commands import Command

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    level=logging.WARNING)

logger = logging.getLogger('debug_print')


class Start(Command):
    """Returns all usable commands of this bot. Is called when /start is sent to the bot."""

    def __init__(self, update, context):
        super().__init__(update, context)
        start_string = ("/help {command}\n"
                        "/login {password}\n"
                        "/search {query}\n"
                        "/start\n\n"
                        "Send data to me and I will store it for you")
        self.answer(start_string)


class Help(Command):
    """Returns all help text to every possible command.

    Example:
        If the bot recives '/help start' it will return the help text for the
        start command.

     Is called when /help is sent to the bot.
     """

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
            else:
                self.answer(("Use one of the following arguments: "
                             "start, login, search, get."
                             "\n\n Or send a file to store it."))


class Login(Command):
    """Returns success message if password was correct.

    Infos:
        The password recived as a argument to the /login command
        is matched with the bot_access_password imported from
        settings.py 

     Is called when /login {password} is sent to the bot.
     """

    def __init__(self, update, context):
        super().__init__(update, context)
        self.check_args()
        if self.check:
            submitted_pw = self.arg
            if submitted_pw == bot_access_password:
                self.request.authorize_user()
                self.answer("Login successful")
            else:
                self.answer("Wrong password")


class Search(Command):
    """Returns the result of the search query.

    Info:
        If the bot recives /search without argumets, 
        infos to every file available will be returned.
        The data returne will be displayed as buttons,
        if you click the button the ButtonPressed class
        is called.

     Is called when /search {query} is sent to the bot.
     """

    def __init__(self, update, context):
        super().__init__(update, context)
        self.search_args = []
        self.arg_parse = True
        if self.request.user.authorized:
            self.get_search_args()
            if self.arg_parse:
                if self.search_args:
                    self.answer("\n".join([i[0] + " " + i[1]
                                           for i in self.search_args]) + "a")
                else:
                    files = self.request.get_all_files()
                    self.send_file_buttons(files)
            else:
                self.answer(
                    "There is a problem with your search query.\n\nRead /help search")
        else:
            self.answer(
                "You need to be logged in to search files \n/login {password}")

    def send_file_buttons(self, files):
        """Creates a InlineKeyboard with buttons to the files."""
        keyboard = InlineKeyboardMarkup(
            [self.get_file_button(file) for file in files])
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id, text="Your search results", reply_markup=keyboard)

    def get_file_button(self, file):
        """Returns a button to a file. If clicked the ButtonPressed class is called"""
        button = InlineKeyboardButton(
            f"{file.file_name}\n ({file.saved})", callback_data=f"{file.id}")
        return [button]

    def get_search_args(self):
        """Checks for all the possible search parameter in the query"""
        args = self.context.args
        if "name" in args:
            self.get_arg_and_param("name", args)
        if "date" in args and self.arg_parse:
            self.get_arg_and_param("date", args)
        if "type" in args and self.arg_parse:
            self.get_arg_and_param("type", args)
        if "user" in args and self.arg_parse:
            self.get_arg_and_param("user", args)
        if "extension" in args and self.arg_parse:
            self.get_arg_and_param("extension", args)

    def get_arg_and_param(self, arg, args):
        """Adds the search parameter and value pair to the search_args list"""
        pos = args.index(arg)
        try:
            param = args[pos+1]
            self.search_args.append((arg, param))
        except Exception as e:
            self.arg_parse = False
            logger.warning(e)


class Doc(Command):
    """Returns a success message if recived the file was saved successfully.

    Info:
        If the bot recives one of the supportet files
        the file will be saved. Meta data of the file
        are saved in the databse.

     Is called when the bot recives a file of type: document, video, photo, audio.
     """

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
                "You need to be logged in to upload files \n/login {password}")


class ButtonPressed(Command):
    """Returns requested the file.

     Is called when the a button sent as a search restult is clicked.
     """

    def __init__(self, update, context):
        date = datetime.datetime.now()
        chat = Chat(update._effective_chat.id, "private")
        update.message = Message(0, date, chat)
        super().__init__(update, context)
        query = self.update.callback_query
        query.answer()
        self.data = query.data

        file = self.request.return_file(self.data)
        file_data = self.storage_handler.storage.read(file.unique_name)
        if file.file_type == "photo":
            self.context.bot.send_photo(
                chat_id=self.update.effective_chat.id, photo=file_data)
        elif file.file_type == "document":
            self.context.bot.send_document(
                chat_id=self.update.effective_chat.id, document=file_data)
        elif file.file_type == "video":
            self.context.bot.send_video(
                chat_id=self.update.effective_chat.id, video=file_data)
        elif file.file_type == "audio":
            self.context.bot.send_audio(
                chat_id=self.update.effective_chat.id, audio=file_data)


if __name__ == "__main__":
    # Set all the event handlers of the bot.

    updater = Updater(token=telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', Start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', Help)
    dispatcher.add_handler(help_handler)

    login_handler = CommandHandler('login', Login)
    dispatcher.add_handler(login_handler)

    search_handler = CommandHandler('search', Search)
    dispatcher.add_handler(search_handler)

    filters = [Filters.photo, Filters.video, Filters.audio, Filters.document]
    for filter in filters:
        handler = MessageHandler(filter, Doc)
        dispatcher.add_handler(handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(ButtonPressed))

    logger.warning("Bot is listening...")
    updater.start_polling()
