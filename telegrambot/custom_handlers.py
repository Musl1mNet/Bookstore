from telegram import Update
from telegram.ext import BaseHandler


class UserHandler(BaseHandler):
    def check_update(self, update: object):
        return isinstance(update, Update) and update.effective_user