from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from django.conf import settings
from django.db import connection
from datetime import datetime
import os
import pathlib
import time

class Command(BaseCommand):
    def start_handler(self, update, context):
        update.message.reply_text('Salom')
    def save_handler(self, update: Update, context):
        n = 1
        while True:
            file_name = settings.USER_ROOT / f"user_{n}.txt"
            if not file_name.is_file():
                break
            n += 1
        with open(file_name, "w") as f:
                f.write(update.effective_message.text)
        update.callback_query.answer(text="Ma'lumot saqlandi!☑", show_alert=True)
        update.effective_message.delete()
    def delete_handler(self, update: Update, context):
        update.callback_query.answer(text="Ma'lumot o'chirildi!☑", show_alert=True)
        img =   update.effective_message.text[update.effective_message.text.index("/img/") + 5:].split("\n")[0]
        img = pathlib.Path(settings.MEDIA_ROOT / f"{img}")
        img.unlink()
        update.effective_message.delete()
    def publish_book(self, update: Update, context: CallbackContext):
        id  = context.match.group(1)
        update.callback_query.answer(text="Kitob chop qilindi!☑", show_alert=True)
        query = f"""UPDATE books SET status = 1 WHERE id = {id};"""
        with connection.cursor() as c:
            c.execute(query)
        update.effective_message.delete()

    def unpublish_book(self, update: Update, context: CallbackContext):
        id = context.match.group(1)
        update.callback_query.answer(text="Chop qilish bekor qilindi!")
        query = f"""UPDATE books SET status = 2 WHERE id = {id};"""
        with connection.cursor() as c:
            c.execute(query)
        update.effective_message.delete()

    def handle(self, *args, **options):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', self.start_handler))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.save_handler, pattern="^save$"))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.delete_handler, pattern="^delete$"))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.publish_book, pattern="^publish_(\d+)"))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.unpublish_book, pattern="^unpublish_(\d+)"))
        print(updater.bot.getUpdates)
        updater.start_polling()
        updater.idle()