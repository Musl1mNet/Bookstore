from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from django.utils.translation import gettext as _

from telegrambot.models import TelegramUser


async def account_login(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user: TelegramUser = context.tguser
    if user.user_id:
        await update.effective_message.reply_text(_("Siz login bo'lgansiz!"))
        return
    await update.effective_message.reply_text(_("Login:parol ko'rinishida jo'nating"))
    context.user_data["login"] = True

async def account_login_check(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("login"):
        return

    username, password = update.effective_message.text.split(":")

    try:
        user = await User.objects.aget(username=username)
        if check_password(password, user.password):
            context.tguser.user_id = user.id
            await context.tguser.asave()
    except:
        pass

    await update.effective_message.delete()

    if context.tguser.user_id is not None:
        await update.effective_message.reply_text("Siz muvaffaqiyatli login bo'ldingiz")
    else:
        await update.effective_message.reply_text("Login va/yoki parol noto'g'ri")



handlers = [
    CommandHandler("login", account_login),
    (MessageHandler(filters.ALL & ~filters.COMMAND & filters.Regex(':'), account_login_check), 52)
]