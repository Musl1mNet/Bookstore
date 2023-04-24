import datetime

from django.core.management import BaseCommand
from django.conf import settings
from django.utils.translation import gettext_lazy as _, activate as lang_activate, get_language
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler, ApplicationBuilder, MessageHandler, filters, InlineQueryHandler
from asgiref.sync import sync_to_async
from catalog.models import Country, Book, Category, Language, Author, User
STATE = 'state'
STATE_LANGUAGE = 'language'
STATE_ADD = 'book-add'
STATE_ADD_NAME = 'book-add-name'
STATE_ADD_CONTENT = 'book-add-content'
STATE_ADD_PHOTO = 'book-add-photo'
STATE_ADD_PRICE = 'book-add-price'
STATE_ADD_STATUS = 'book-add-status'
STATE_ADD_PUBLISH_YEAR = 'book-add-publish_year'
STATE_ADD_COUNTRY = 'book-add-country'
STATE_ADD_CATEGORY = 'book-add-category'
STATE_ADD_LANGUAGE = 'book-add-language'
STATE_ADD_AUTHOR = 'book-add-author'
STATE_SAVE = "book-save"
ADD_QUESTIONS = {"hi": _("Salom botimizga xush kelibsiz!\nXizmat sifatini yaxshilash uchun sizga kerakli tilni\n/languages buyrug'i orqali sozlang!")
                ,"name":_("Kitob nomini kiriting!"), "content":_("Kitobga ta'rif bering!"),
                  "photo":_("Kitob rasmini jo'nating!"), "photo1":_("Kitob rasmini kiritasizmi?"),
                  "price":_("Kitob narxini kiriting!"), "status":_("Kitobning statusini tanlang!"),
                  "publish_year":_("Kitob chop qilingan yilni kiriting!"), "publish_year1":_("Chop qilingan yili bormi?"),
                  "category":_("Kitob kategoriyasi?"), "language":_("Kitob chop qilingan til?"),
                  "country":_("Chop qilingan davlati?"), "author":_("Kitob aftorini tanlang!"),
                  "author1":_("Yana Avtor qo'shasizmi?"), "save_agr":_("Ma'lumotlarni saqlaysizmi?"), "save": _("📁 Ma'lumotlarni saqlash"),
                  "data_success":_("Ma'lumotlarni muvofaqiyatli to'ldirdingiz!\nMalumotlarni saqlash uchun pastdagi tugmani bosing!"),
                 "success": _('Muvofaqiyatli!'), "choose_lang": _("Kerakli tilni tanlang!")
                }
PERM = {"nostart": _("Hurmatli foydalanuvchi oldin /start buyrug'ini kiriiting"),"common_format_err":_("Hurmatli foydalanuvchi siz noto'g'ri formatda"
                            " ma'lumot kirityapsiz iltimos malumotni to'g'ri kiriting"),
        "min_price_err":_("Kitob narxining eng kichik qiymati: 1000\n"
                        "Iltimos kattaroq summa kiriting!"),
        "price_type_err":_("Iltimos harf va belgi aralashtirmasdan\n"
                        "Faqat son kiriting! Misol uchun: 23500"),
        "year_type_err":_("Iltimos harf va belgi aralashtirmasdan\nFaqat raqamlar kiriting!"),
        "year_format_err":_("Iltimos yil YYYY formatda kiriting\nMisol uchun: \n2020"),
        "max_year_err":_("Siz kiritgan yil hozirgi yildan katta bo'lmasligi kerak!\nIltimos qayta urining"),
        "yes": _("Ha"), "no": _("Yo'q"), "nstat": _('Yangi'), "pstat": _('Qabul qilingan'), "rstat": _('Inkor qilingan')
        }
BOOK = {"common": _("Kotob ma'lumotlari"), "name": _("Kitob nomi"),
            "content": _("Kitob ta'rifi"), "price": _("Kitob narxi"),
            "status": _("Kitob statusi raqami"), "publish_year": _("Kitob chop qilingan yili"),
            "category": _("Kitob kategoriya"), "language": _("Kitob chiqarilgan til"),
            "country": _("Kitob chiqarilgan davlat"), "authors": _("Kitob aftorlari"),
            "uagr": _("Ko'rsatilgan ma'lumotlarni saqlaysizmi?"), "success_save": _("😅 Ma'lumot muvofaqiyatli saqlandi!\nYana qo'shishni hohlasangiz\n/add komondasini ustiga bosing!"),
        "success_delete": _("🤕 Ma'lumotlar o'chirildi!\nYana qo'shishni hohlasangiz\n/add komondasini ustiga bosing!"),"not_show": _("Ko'rsatilmagan")}
class Command(BaseCommand):
    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = update.effective_user
        try:
            user = await User.objects.aget(telegram_id = user_data.id)
        except User.DoesNotExist:
            lang_code = [user_data.language_code if user_data.language_code in set([row[0] for row in settings.LANGUAGES]) else "uz"]
            user = await User.objects.acreate(telegram_id = user_data.id,
                                              first_name = user_data.first_name,
                                              last_name = user_data.last_name,
                                              username = user_data.username,
                                              language = lang_code[0])
        lang_activate(user.language)
        await update.message.reply_text(f"""{ADD_QUESTIONS["hi"]}""")
        context.user_data[STATE] = STATE_LANGUAGE
    async def lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        usr_id = update.effective_user.id
        try:
            user = await User.objects.aget(telegram_id=usr_id)
        except User.DoesNotExist:
            await update.effective_message.reply_text(f"""{PERM["nostart"]}""")
            return
        try:
            user.language = context.match.group(1)
            await sync_to_async(user.save)()
            lang_activate(user.language)
            await update.callback_query.answer(f"""{ADD_QUESTIONS["success"]}""")
            await update.effective_message.delete()
            return
        except AttributeError:
            lang_activate(user.language)
            reply_button = await self.get_data(user)
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["choose_lang"]}""", reply_markup=reply_button)
    async def get_data(self, usr: User):
        btn_txt = zip(["✅" + row[1]  if row[0] == usr.language else row[1] for row in settings.LANGUAGES], [row[0] for row in settings.LANGUAGES])
        btn = []
        for txt in btn_txt:
            btn.append(
                [InlineKeyboardButton(txt[0], callback_data=f'language_{txt[1]}')]
            )
        return InlineKeyboardMarkup(btn)
    async def add_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        usr_id = update.effective_user.id
        try:
            user = await User.objects.aget(telegram_id=usr_id)
        except User.DoesNotExist:
            await update.effective_message.reply_text(f"""{PERM["nostart"]}""")
            return
        lang_activate(user.language)
        context.user_data[STATE] = STATE_ADD_NAME
        await update.message.reply_text(f"""{ADD_QUESTIONS["name"]}""")

    async def msg_handler(self,  update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.effective_message.text
        txt = update.effective_message.text
        photo = update.effective_message.photo
        st = context.user_data.get(STATE, "")
        if (st != STATE_ADD_PHOTO and photo) or (st == STATE_ADD_PHOTO and txt):
            await update.message.reply_text(f"""{PERM["common_format_err"]}""")
            return

        if st == STATE_ADD_NAME:
            context.user_data['book'] = {"name": msg}
            context.user_data[STATE] = STATE_ADD_CONTENT
            await update.message.reply_text(f"""{ADD_QUESTIONS["content"]}""")

        elif st == STATE_ADD_CONTENT:
            context.user_data['book'].update({"content": msg})
            context.user_data[STATE] = STATE_ADD_PHOTO
            if context.user_data[STATE] == STATE_ADD_PHOTO:
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["photo1"]}""",
                reply_markup=InlineKeyboardMarkup(
                    [[
                    InlineKeyboardButton(f"""✅ {PERM["yes"]}""", callback_data=f'book_add_photo_{1}'),
                    InlineKeyboardButton(f"""❌ {PERM["no"]}""", callback_data=f'book_add_photo_{0}')
                    ]]))
        elif st == STATE_ADD_PHOTO:
            file_id = update.message.photo[-1].file_id
            context.user_data["book"].update({"photo": file_id})
            file = await context.bot.get_file(file_id)
            context.user_data["book"].update({"photo_root": "books/" + file.file_path.split("/")[-1] })
            context.user_data[STATE] = STATE_ADD_PRICE
            await update.message.reply_text(f"""{ADD_QUESTIONS["price"]}""")

        elif st == STATE_ADD_PRICE:
            STATUS_NEW = 0
            STATUS_PUBLISHED = 1
            STATUS_REJECTED = 2

            if msg.isdigit():
                if int(msg) <= 1000:
                    await update.effective_message.reply_text(f"""{PERM["min_price_err"]}""")
                    return
                context.user_data['book'].update({"price": int(msg)})
                context.user_data[STATE] = STATE_ADD_STATUS
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["status"]}""",
                    reply_markup=InlineKeyboardMarkup(
                    [
                    [InlineKeyboardButton(f"""⏳ {PERM["nstat"]}""", callback_data=f'book_add_status_{STATUS_NEW}')],
                    [InlineKeyboardButton(f"""✅ {PERM["pstat"]}""", callback_data=f'book_add_status_{STATUS_PUBLISHED}')],
                    [InlineKeyboardButton(f"""❌ {PERM["rstat"]}""", callback_data=f'book_add_status_{STATUS_REJECTED}')]
                    ]))
                return
            await update.effective_message.reply_text(f"""{PERM["price_type_err"]}""")
            return
        elif st == STATE_ADD_PUBLISH_YEAR:
            if msg.isdigit():
                if len(msg) != 4:
                    await update.effective_message.reply_text(f"""{PERM["year_format_err"]}""")
                    return
                elif int(msg) > datetime.datetime.now().year:
                    await update.effective_message.reply_text(f"""{PERM["max_year_err"]}""")
                    return
                context.user_data["book"].update({"publish_year": int(msg)})

                context.user_data[STATE] = STATE_ADD_CATEGORY
                buttons = []
                categories = await sync_to_async(lambda: [row for row in Category.objects.order_by(f"name").all()])()
                for c in categories:
                    buttons.append(
                        [InlineKeyboardButton(c.name, callback_data=f'book_add_category_{c.id}')]
                    )
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["category"]}""",
                    reply_markup=InlineKeyboardMarkup(buttons))
                return
            await update.effective_message.reply_text(f"""{PERM["year_type_err"]}""")

        return

    async def book_add_photo_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        if st == STATE_ADD_PHOTO:
            if context.match.group(1) == str(1):
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["photo"]}""")
                return
            context.user_data[STATE] = STATE_ADD_PRICE
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["price"]}""")
        return

    async def book_add_status_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        if st == STATE_ADD_STATUS:
            context.user_data["book"].update({"status": int(context.match.group(1))})
            context.user_data[STATE] = STATE_ADD_PUBLISH_YEAR
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["publish_year1"]}""",
                reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"""✅ {PERM["yes"]}""", callback_data=f'book_add_publish_year_{1}'),
                 InlineKeyboardButton(f"""❌ {PERM["no"]}""", callback_data=f'book_add_publish_year_{0}')
                ]]))


    async def book_add_publish_year_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        if st == STATE_ADD_PUBLISH_YEAR:
            if context.match.group(1) == str(1):
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["publish_year"]}""")
                return
            context.user_data[STATE] = STATE_ADD_CATEGORY
            buttons = []
            categories = await sync_to_async(lambda: [row for row in Category.objects.order_by(f"name").all()])()
            for c in categories:
                buttons.append(
                    [InlineKeyboardButton(c.name, callback_data=f'book_add_category_{c.id}')]
                )
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["category"]}""",
                reply_markup=InlineKeyboardMarkup(buttons))
        return

    async def book_add_category_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        if st == STATE_ADD_CATEGORY:
            context.user_data["book"].update({"category": int(context.match.group(1))})
            context.user_data[STATE] = STATE_ADD_LANGUAGE
            buttons = []
            categories = await sync_to_async(lambda: [row for row in Language.objects.order_by('name').all()])()
            for c in categories:
                buttons.append(
                    [InlineKeyboardButton(c.name, callback_data=f'book_add_language_{c.id}')]
                )
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["language"]}""",
                reply_markup=InlineKeyboardMarkup(buttons))
        return
    async def book_add_language_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        st = context.user_data.get(STATE, "")
        await update.effective_message.delete()
        if st == STATE_ADD_LANGUAGE:
            context.user_data["book"].update({"language": int(context.match.group(1))})
            context.user_data[STATE] = STATE_ADD_COUNTRY
            buttons = []
            countries = await sync_to_async(lambda: [row for row in Country.objects.order_by('name').all()])()
            for c in countries:
                buttons.append(
                    [InlineKeyboardButton(c.name, callback_data=f'book_add_country_{c.id}')],

                )
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["country"]}""",
                reply_markup=InlineKeyboardMarkup(buttons))
        return
    async def book_add_country_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        if st == STATE_ADD_COUNTRY:
            context.user_data["book"].update({"country": int(context.match.group(1))})
            context.user_data[STATE] = STATE_ADD_AUTHOR
            context.user_data["book"]["authors"] = []
            buttons = []
            authors = await sync_to_async(lambda: [row for row in Author.objects.order_by('name').all()])()
            for a in authors:
                buttons.append(
                    [InlineKeyboardButton(a.name, callback_data=f'book_add_author_{a.id}')],

                )
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["author"]}""",
                reply_markup=InlineKeyboardMarkup(buttons))
        return

    async def book_add_author_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        q = len(context.match.group().split('_'))
        context.match.groups()
        if st == STATE_ADD_AUTHOR and q == 5:
            selected_authors  = []
            buttons = []
            context.user_data["book"]["authors"].append(int(context.match.group(2)))
            selected_authors = context.user_data["book"]["authors"]
            if int(context.match.group(1)) == 1:
                authors = await sync_to_async(lambda: [row for row in Author.objects.order_by('name').exclude(id__in = selected_authors).all()])()
                for a in authors:
                    buttons.append(
                        [InlineKeyboardButton(a.name, callback_data=f'book_add_author_{a.id}')],

                    )
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["author"]}""",
                    reply_markup=InlineKeyboardMarkup(buttons))
            else:
                context.user_data["book"].update({"authors": selected_authors})
                context.user_data[STATE] = STATE_SAVE
                await update.effective_message.reply_text(f"""{ADD_QUESTIONS["data_success"]}""",
                                                          reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"""{ADD_QUESTIONS["save"]}""", callback_data=f'book_save'),
                ]]))
        elif st == STATE_ADD_AUTHOR and q == 4:
            selected_author = context.match.group(1)
            await update.effective_message.reply_text(f"""{ADD_QUESTIONS["author1"]}""",
                reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"""✅ {PERM["yes"]}""", callback_data=f'book_add_author_{1}_{selected_author}'),
                 InlineKeyboardButton(f"""❌ {PERM["no"]}""", callback_data=f'book_add_author_{0}_{selected_author}')
                ]]))
        return



    async def book_save_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.effective_message.delete()
        st = context.user_data.get(STATE, "")
        book = context.user_data.get("book", {})
        photo = book.get("photo", "")
        category =  await Category.objects.aget(id = book["category"])
        language =  await Language.objects.aget(id = book["language"])
        country =  await Country.objects.aget(id = book["country"])
        authors =  [await Author.objects.aget(id = author_id) for author_id in book["authors"]]
        if not photo:
            photo = f"{settings.MEDIA_ROOT}/default.jpg"
        elif context.match.group() != "book_save" and context.match.group(1) == "1":
            file = await context.bot.get_file(photo)
            await file.download_to_drive(f"{settings.MEDIA_ROOT}/{book.get('photo_root')}")
        publish_year = book.get("publish_year", BOOK["not_show"])
        if st == STATE_SAVE and book and context.match.group() == "book_save":
            caption = (
                f"""⚠ {BOOK["common"]}\n"""
                f"""{BOOK["name"]}: {book.get('name')}\n"""
                f"""{BOOK["content"]}: {book.get('content')}\n"""
                f"""{BOOK["price"]}: {book.get('price')}\n"""
                f"""{BOOK["status"]}: {book.get('status')}\n"""
                f"""{BOOK["publish_year"]} : {publish_year}\n"""
                f"""{BOOK["category"]} : {category.name}\n"""
                f"""{BOOK["language"]} : {language.name}\n"""
                f"""{BOOK["country"]} : {country.name}\n"""
                f"""{BOOK["authors"]} : {[a.name for a in authors]}\n\n"""
                f"""{BOOK["uagr"]}"""
            )
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"""✅ {PERM["yes"]}""", callback_data=f"book_save_{1}"),
                        InlineKeyboardButton(f"""❌ {PERM["no"]}""", callback_data=f"book_save_{0}"),
                    ]
                ]
            )
            await update.effective_message.reply_photo(photo, caption=caption, reply_markup=reply_markup)
        elif context.match.group(1) == "1":
            obj = await Book.objects.acreate(
            name=book["name"],
            content = book["content"],
            photo = book.get("photo_root", "default.jpg"),
            price = book["price"],
            status = book["status"],
            publish_year = book.get("publish_year"),
            category =  category,
            language = language,
            country = country
            )
            await sync_to_async(obj.authors.set)(book["authors"])

            await update.effective_message.reply_text(f"""{BOOK["success_save"]}""")
        else:
            book.clear()
            await update.effective_message.reply_text(f"""{BOOK["success_delete"]}""")
        return

    async def book_inline_search_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.inline_query.query
        books = await sync_to_async(lambda: [row for row in Book.objects.select_related('country', 'category', 'language').prefetch_related('authors').filter(name = query).order_by('name').all()])()
        buttons = []
        for b in books:
            caption = (
                f"""📃 {BOOK["common"]}\n"""
                f"""{BOOK["name"]}: {b.name}\n"""
                f"""{BOOK["content"]}: {b.content}\n"""
                f"""{BOOK["price"]}: {b.price}\n"""
                f"""{BOOK["publish_year"]} : {BOOK["not_show"] if not b.publish_year else b.publish_year}\n"""
                f"""{BOOK["category"]} : {b.category.name}\n"""
                f"""{BOOK["language"]} : {b.language.name}\n"""
                f"""{BOOK["country"]} : {b.country.name}\n"""
            )
            buttons.append(InlineQueryResultArticle(f"{b.id}", f"{b.name}", InputTextMessageContent(caption)))
        await update.inline_query.answer(buttons)

    def handle(self, *args, **options):
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start_handler))
        app.add_handler(CommandHandler("languages", self.lang_handler))
        app.add_handler(CommandHandler("add", self.add_handler))
        app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO & ~filters.COMMAND, self.msg_handler))
        app.add_handler(InlineQueryHandler(self.book_inline_search_handler))
        app.add_handler(CallbackQueryHandler(self.lang_handler, "^language_([a-z]+)"))
        app.add_handler(CallbackQueryHandler(self.book_add_photo_handler, "^book_add_photo_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_status_handler, "^book_add_status_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_publish_year_handler, "^book_add_publish_year_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_category_handler, "^book_add_category_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_language_handler, "^book_add_language_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_country_handler, "^book_add_country_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_author_handler, "^book_add_author_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_add_author_handler, "^book_add_author_(\d+)_(\d+)$"))
        app.add_handler(CallbackQueryHandler(self.book_save_handler, "^book_save$"))
        app.add_handler(CallbackQueryHandler(self.book_save_handler, "^book_save_(\d+)$"))

        app.run_polling()