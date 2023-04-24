#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""Basic example for a bot that can receive payment from user."""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

PAYMENT_PROVIDER_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    msg = (
        "Use /shipping to get an invoice for shipping-payment, or /noshipping for an "
        "invoice without shipping."
    )

    await update.message.reply_text(msg)


async def start_with_shipping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an invoice with shipping-payment."""
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    currency = "USD"
    # price in dollars
    price = 1
    # price * 100 so as to include 2 decimal points
    # check https://core.telegram.org/bots/payments#supported-currencies for more details
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    await context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        PAYMENT_PROVIDER_TOKEN,
        currency,
        prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


async def start_without_shipping_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends an invoice without shipping-payment."""
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    currency = "USD"
    # price in dollars
    price = 1
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    await context.bot.send_invoice(
        chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
    )


async def shipping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption("1", "Shipping Option A", [LabeledPrice("A", 100)])]
    # second option has an array of LabeledPrice objects
    price_list = [LabeledPrice("B1", 150), LabeledPrice("B2", 200)]
    options.append(ShippingOption("2", "Shipping Option B", price_list))
    await query.answer(ok=True, shipping_options=options)


# after (optional) shipping, it's the pre-checkout
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


# finally, after contacting the payment provider...
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    await update.message.reply_text("Thank you for your payment!")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5939657540:AAElQjD_oAacRLNB-tVHtqYpvTQ8JvrgS7U").build()

    # simple start function
    application.add_handler(CommandHandler("start", start_callback))

    # Add command handler to start the payment invoice
    application.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    application.add_handler(CommandHandler("noshipping", start_without_shipping_callback))

    # Optional handler if your product requires shipping
    application.add_handler(ShippingQueryHandler(shipping_callback))

    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    application.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()


































# from django.core.management.base import BaseCommand
# from telegram.ext import Updater
# from django.conf import settings
# from datetime import datetime
# import pathlib
# import time

# class Command(BaseCommand):

#     def handle(self, *args, **options):
#         updater = Updater(settings.TELEGRAM_BOT_TOKEN)
#         all_app_stat = dict()
#         for app in settings.INSTALLED_APPS:
#             if "." in app:
#                 continue
#             files = pathlib.Path(settings.BASE_DIR / app).rglob("*.py")
#             apps_stat = {app: {"total_lines": 0, "total_files": 0}}
#             total_lines = 0
#             total_files = 0
#             for file in files:
#                 with open(f"{file}", "r") as f:
#                     for n_line, kms in enumerate(f, 1):
#                         pass
#                 total_lines += n_line
#                 total_files += 1
#             apps_stat[app]["total_lines"] = total_lines
#             apps_stat[app]["total_files"] = total_files
#             total_lines, total_files = 0, 0
#             all_app_stat.update(apps_stat)
#         for key, val in all_app_stat.items():
#             print(f"App nomi {str(key).upper()}\nJami fayllar {val['total_files']} ta\nJami kodlar {val['total_lines']} qator")
#         files_mtime = {}
#         is_scan = True
#         while True:
#             cp_mtime = files_mtime.copy()

#             for app in settings.INSTALLED_APPS:
#                 if "." in app:
#                     continue
#                 files = list(pathlib.Path(settings.BASE_DIR / app).rglob("*.py"))
#                 for f in files:
#                     st = f.lstat()
#                     mtime = datetime.fromtimestamp(st.st_mtime)
#                     mtime_str = f"{mtime:%d.%m.%Y %H:%M:%S}"
#                     if is_scan:
#                         pass
#                     elif f.name not in files_mtime:
#                         updater.bot.send_message(chat_id=settings.CHAT_ID,
#                                                  text=f"{f.parent.name} ga {f.name} nomli fayl qo'shildi")
#                     elif files_mtime[f.name] != mtime_str:
#                         updater.bot.send_message(chat_id=settings.CHAT_ID,
#                                                  text=f"{f.parent.name} dagi {f.name} faylda o'zgarish")
#                     files_mtime[f.name] = mtime_str
#                     if f.name in cp_mtime:
#                         del cp_mtime[f.name]
#             is_scan = False
#             if cp_mtime:
#                 for del_f, _ in cp_mtime.items():
#                     updater.bot.send_message(chat_id=settings.CHAT_ID,
#                                              text=f"{del_f} fayl o'chirildi")
#                     del cp_mtime[del_f]

#             time.sleep(1)
