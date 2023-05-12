from django.conf import settings
from telegram.ext import ApplicationBuilder

from telegrambot.handlers import handlers

app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

for h in handlers:
    if isinstance(h, tuple):
        app.add_handler(*h)
    else:
        app.add_handler(h, 50)