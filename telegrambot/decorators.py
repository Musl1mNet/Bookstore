from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from telegram import Update
from telegram.ext import ContextTypes


def tg_login_required(fn):
    async def wrapper(update:Update, context:ContextTypes):
        if context.tguser.user_id is None:
            if update.callback_query:
                await update.callback_query.answer("Ruxsat berilmadi")
                return
            else:
                await update.effective_message.reply_text("Ruxsat berilmadi")
                return

        return await fn(update,context)

    return wrapper

@sync_to_async
def has_perms(user:User, *perms):
    return user.has_perms(*perms)
def tg_permission_required(*perms):
    def cb(fn):
        async def wrapper(update:Update, context:ContextTypes):
            if not hasattr(context, "user"):
                context.user = await User.objects.aget(id=context.tguser.user_id)
            access = await has_perms(context.user, *perms)
            if not access:
                if update.callback_query:
                    await update.callback_query.answer("Ruxsat berilmadi")
                    return
                else:
                    await update.effective_message.reply_text("Ruxsat berilmadi")
                    return

            return await fn(update, context)

        return wrapper
    return cb