from middleware import Request


class Command:
    def __init__(self, update, context):
        self.update = update
        self.context = context
        self.request = Request(update)
        self.check = True

    def check_args(self):
        if len(self.context.args) == 0:
            self.check = False
            self.answer("No arguments provided")
        elif len(self.context.args) > 1:
            self.check = False
            self.answer("Too many arguments")
        else:
            self.arg = self.context.args[0]

    def answer(self, text):
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id, text=text)
