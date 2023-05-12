from django.conf import settings
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from django.utils.translation import get_language, gettext as _, activate as set_current_language

from telegrambot.custom_handlers import UserHandler
from telegrambot.models import TelegramUser


async def telegram_user_load(update:Update, context:ContextTypes.DEFAULT_TYPE):

    tg, _ = await TelegramUser.objects.aget_or_create(defaults={
        "username": update.effective_user.username,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name,
        "language": update.effective_user.language_code,
    }, telegram_user_id = update.effective_user.id)
    sys_languages = set([row[0] for row in settings.LANGUAGES])
    context.tguser = tg

    set_current_language(tg.language if tg.language in sys_languages else get_language())

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE, edit=False):
    params = {"text": _("Xush kelibsiz {}").format(update.effective_user.first_name),
              "reply_markup": InlineKeyboardMarkup([[b for b in [
                      InlineKeyboardButton("🇺🇿", callback_data="uz"),
                      InlineKeyboardButton("🇷🇺", callback_data="ru"),
                      InlineKeyboardButton("🇺🇸", callback_data="en")
                  ] if b.callback_data != get_language()
              ]])
    }

    if edit:
        try:
            await update.effective_message.edit_text(**params)
        except:
            await update.effective_message.delete()
            await update.effective_message.reply_text(**params)
    else:
        await update.effective_message.reply_text(**params)

async def change_language(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user: TelegramUser = context.tguser
    user.language = context.match.group(1)
    await user.asave()

    set_current_language(user.language)

    await update.callback_query.answer(_("Muvaffaqiyatli o'zgardi"))

    await start(update, context, True)

handlers = [
    (UserHandler(telegram_user_load), 0),
    CommandHandler("start", start),
    CallbackQueryHandler(change_language, pattern="^(uz|ru|en)$")
]