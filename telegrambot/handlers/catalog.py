from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from django.utils.translation import gettext as _

from catalog.models import Category, Book
from telegrambot.decorators import tg_login_required


async def catalog_category_list(update:Update, context:ContextTypes.DEFAULT_TYPE):
    buttons = []
    parent_id = context.match.group(1) if context.match and len(context.match.groups()) > 0 else None
    parent = None if parent_id is None else await Category.objects.aget(id=parent_id)
    async for cat in Category.objects.filter(parent_id=parent_id).order_by("id").all():
        buttons.append(
            InlineKeyboardButton(cat.name, callback_data=f"catalog_{cat.id}")
        )
    has_children = len(buttons) > 0
    if parent is not None:
        cb = f"catalog_{parent.parent_id}" if parent.parent_id is not None else "catalog"
        buttons.append(
            InlineKeyboardButton("⬅ " + _("Orqaga"), callback_data=cb)
        )
    if has_children:
        text = []
        params = {
            "text": "\n".join(text + [_("Kategoriyani tanlang")]),
            "reply_markup": InlineKeyboardMarkup(
                [buttons[i:i + 1] for i in range(0, len(buttons))]
            )
        }
    else:
        text = []
        n = 1
        async for book in Book.objects.filter(category_id=parent.id).order_by().all():
            text.append(f"{n}." + book.name)
            buttons.append(
                InlineKeyboardButton(str(n), callback_data=f"book_{book.id}")
            )
            n += 1
        params = {
            "text": "\n".join(text + [_("Kitobni tanlang")]),
            "reply_markup": InlineKeyboardMarkup(
                [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
            )
        }
    if update.callback_query:
        try:
            await update.effective_message.edit_text(**params)
        except:
            await update.effective_message.delete()
            await update.effective_message.reply_text(**params)
    else:
        await update.effective_message.reply_text(**params)
@tg_login_required
async def catalog_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Uraaaa")

handlers = [
    CommandHandler("catalog", catalog_category_list),
    CommandHandler("private", catalog_private),
    CallbackQueryHandler(catalog_category_list, pattern=r"^catalog$"),
    CallbackQueryHandler(catalog_category_list, pattern=r"^catalog_(\d+)$")
]