"""This module contains an object that represents a Telegram Command."""

from middleware import Request
from storage import StorageHandler


class Command:
    """This is the base class for every telegram command used by the bot"""

    def __init__(self, update, context):
        self.update = update
        self.context = context
        self.request = Request(update)
        self.check = True
        self.storage_handler = StorageHandler()

    def check_args(self):
        """Sets check to true if a argument is provided"""
        if len(self.context.args) == 0:
            self.check = False
            self.answer("No arguments provided")
        elif len(self.context.args) > 1:
            self.check = False
            self.answer("Too many arguments")
        else:
            self.arg = self.context.args[0]

    def answer(self, text):
        """Short cut to send a message to the active chat

        Args:
            text (str): The text that is sent as a answer
        """
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id, text=text)
