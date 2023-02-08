import datetime
from django.shortcuts import render, resolve_url
from django.http import HttpResponse, FileResponse
from django.middleware.csrf import get_token
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater
from django.conf import settings
from django.db import connection
from .forms import BooksForm, UserForm
import pathlib
# def registration(request):
    #     form = UserForm()
    #     csrf_token = get_token(request)
    #     reg_send_url = resolve_url("catalog:user-data-send")
    #     return HttpResponse(f"""
    #     <form method = 'post' action = {reg_send_url} enctype = multipart/form-data>
    #         <input type="hidden" name='csrfmiddlewaretoken' value={csrf_token}>
    #         {form.as_p()}
    #         <button type='submit'>Send</button>
    #     </form>
    #     """)
    # def registration_send(request):
    #     print("OK")
    #     first_name = request.POST.get("first_name")
    #     last_name = request.POST.get("last_name")
    #     email = request.POST.get("email")
    #     password = request.POST.get("password")
    #     img = request.FILES.get("img")
    #     file_name = settings.MEDIA_ROOT / img.name
    #     file_url = img.name
    #     index = resolve_url("catalog:users")
    #     if file_name.is_file():
    #         n = 1
    #         while True:
    #             file_url = str(pathlib.Path(str(img.name)[:str(img.name).index(pathlib.Path(img.name).suffix)])) + f"_{n}" + str(pathlib.Path(img.name).suffix)
    #             file_name = settings.MEDIA_ROOT / file_url
    #             if not file_name.is_file():
    #                 break
    #             n += 1
    #     with open(file_name, "wb") as f:
    #         for data in img.chunks():
    #             f.write(data)
    #     resp = f"""
    # First name : {first_name}
    # Last name : {last_name}
    # Email address : {email}
    # User password : {password}
    # Img url : {settings.MEDIA_URL + file_url}
    # """
    #     updater = Updater(settings.TELEGRAM_BOT_TOKEN)
    #     updater.bot.send_message(chat_id= settings.CHAT_ID, text=resp, reply_markup= InlineKeyboardMarkup([
    #         [
    #             InlineKeyboardButton("Saqlash✅", callback_data="save"),
    #             InlineKeyboardButton("O'chirish❌", callback_data="delete")
    #         ]
    #     ]) )
    #     # return HttpResponse(f"ok")
    #     return HttpResponse(f"<a href = '{index}' >Bosh Sahifaga qaytish</a>")
    # def show_users(request):
    #     users = pathlib.Path(settings.USER_ROOT).rglob("*.txt")
    #     resp = []
    #     for user in users:
    #         resp.append(f"<a href = '{user.name}' >{user.name}</a>")
    #     if resp:
    #         return HttpResponse("<br>".join(resp))
    #     else:
    #         return HttpResponse("<h1 style = 'text-align: center;'>User info not found</h1>")
    # def show_file(request, n):
    #     resp = []
    #     with open(settings.USER_ROOT / f"user_{n}.txt", "r") as f:
    #         for line in f.readlines():
    #             if line.split()[0] == "Img":
    #                 url = line[line.index('url') + 6:]
    #                 resp.append(f"""<b>{line.split()[0]}</b> :  <img src='{url}' width='100' height='120' alt= 'Girl in a jacket'>""")
    #                 continue
    #             resp.append(f"<b>{line.split()[0]} {line.split()[1]}</b> : <i>{line.split()[3]}</i>")

    #         return HttpResponse("<br>".join(resp))
    # def book_add(request):
    #     form = BooksForm()
    #     csrf_token = get_token(request)
    #     reg_send_url = resolve_url("catalog:book-data-send")
    #     return HttpResponse(f"""
    #     <form method = 'post' action = '{reg_send_url}' enctype = multipart/form-data>
    #     <input type="hidden" name='csrfmiddlewaretoken' value={csrf_token}>
    #     {form.as_p()}
    #     <button type='submit'>Send</button>
    #     </form>
    #     """)
    # def book_add_send(request):
    #     name = request.POST.get("name")
    #     content = request.POST.get("content")
    #     img = request.FILES.get("photo")
    #     price = request.POST.get("price")
    #     file_name = settings.MEDIA_ROOT / f"book/{img.name}"
    #     file_url = f"book/{img.name}"
    #     books = resolve_url("catalog:books")
    #     if file_name.is_file():
    #         n = 1
    #         while True:
    #             file_url = "book/" + str(
    #                 pathlib.Path(str(img.name)[:str(img.name).index(pathlib.Path(img.name).suffix)])) + f"_{n}" + str(
    #                 pathlib.Path(img.name).suffix)
    #             file_name = settings.MEDIA_ROOT / file_url
    #             if not file_name.is_file():
    #                 break
    #             n += 1
    #     with open(file_name, "wb") as f:
    #         for data in img.chunks():
    #             f.write(data)

    #     query = """INSERT INTO books (name, content, photo, price, status, added_at, updated_at) VALUES (%s, %s, %s, %s, 0, %s, %s);"""
    #     now = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"

    #     with connection.cursor() as c:
    #         c.execute(query,[name, content, settings.MEDIA_URL + file_url, price, now, now])
    #         id = c.lastrowid
    #     updater = Updater(settings.TELEGRAM_BOT_TOKEN)
    #     updater.bot.send_message(chat_id= settings.CHAT_ID, text="Chop qiaymi?", reply_markup= InlineKeyboardMarkup([
    #         [
    #             InlineKeyboardButton("Ha✅", callback_data=f"publish_{id}"),
    #             InlineKeyboardButton("Yo'q❌", callback_data=f"unpublish_{id}")
    #         ]
    #     ]) )
    #     return HttpResponse(f"<a href = '{books}' >Kitoblarni ko'rish</a>")

    # def show_books(request):
    # resp = """
    # <!DOCTYPE html>
    # <html>
    # <style>
    # table, th, td {
    #   border:1px solid black;
    # }
    # </style>
    # <body>
    # <h1 style = 'text-align: center;'>Table of books</h1>
    # <table style = 'width:100%; text-align: center;'>
    #   <thead>
    #     <tr>
    #       <th>Id</th>
    #       <th>Name</th>
    #       <th>Content</th>
    #     </tr>
    #   </thead>
    #   <tbody>"""
    # with connection.cursor() as c:
    #     query = """SELECT id, name, content FROM books WHERE status = 1 ORDER BY id """
    #     c.execute(query)
    #     books = c.fetchall()
    #     for book in books:
    #         id, name, content = book
    #         resp += f"""<tr>
    #       <td>{id}</td>
    #       <td>{name}</td>
    #       <td>{content}</td>
    #     </tr>"""
    # resp += """</tbody></table></body></html>"""
    # return HttpResponse(resp)


def show_books(request):
    books = {}
    txt = ""
    fields = []
    savol = []
    with open(f"{settings.BASE_DIR}/savollar.txt", "r") as s:
        savol = s.readlines()
    if request.POST:
        misol = ""
        if request.POST.get("misol"):
            misol = request.POST.get("misol")
            # print(misol)
            misol = int(misol)
        else:
            with connection.cursor() as c:
                query = "SELECT id, name, content, added_at, status FROM catalog_book ORDER BY id"
                c.execute(query)
                books = c.fetchall()
                fields = ["ID", "Name", "Content", "Added at", "Status"]
                sharti="Barcha kitoblar"
                

        if misol == 1:
            with connection.cursor() as c:
                query = "SELECT id, name, content, added_at, status FROM catalog_book ORDER BY added_at DESC LIMIT 10"
                c.execute(query)
                books = c.fetchall()
                fields = ["ID", "Name", "Content", "Added at", "Status"]
                sharti = savol[misol - 1]

        elif misol == 2:
            with connection.cursor() as c:
                query = """SELECT id, name, content, added_at, `read`, status FROM catalog_book
                    WHERE YEAR(added_at) = YEAR(NOW()) AND `read` = 0;"""
                c.execute(query)
                books = c.fetchall()
                fields = ["ID", "Name", "Content", "Added at", "Read", "Status"]
                sharti = savol[misol - 1]

        elif misol == 3:
            with connection.cursor() as c:
                query = """SELECT id, name, content, added_at, `read`, status FROM catalog_book
                    WHERE YEAR(added_at) = (YEAR(NOW()) - 1) ORDER BY `read` DESC LIMIT 10"""
                c.execute(query)
                books = c.fetchall() 
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Added at", "Read", "Status"]

        elif misol == 4:
            with connection.cursor() as c:
                query = "SELECT COUNT(*) FROM catalog_book WHERE status=1"
                c.execute(query)
                books = c.fetchone() 
                sharti = savol[misol - 1]
                txt = "Qabul qilingan kitoblar soni : "
        elif misol == 5:
            with connection.cursor() as c:
                query = "SELECT id, name, content, language_id, publish_year, status FROM catalog_book WHERE language_id IN(1,2) AND publish_year = 2005 LIMIT 10"
                c.execute(query)
                books = c.fetchall() 
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Language ID", "Publish year", "Status"]

        elif misol == 6:
            with connection.cursor() as c:
                query = "SELECT id, name, content, price, `read` FROM catalog_book ORDER BY price ASC, `read` DESC LIMIT 10"
                c.execute(query)
                books = c.fetchall() 
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Price", "Read"]

        elif misol == 7:
            with connection.cursor() as c:
                query = """SELECT id, name, content, added_at, status, ROUND(rating_stars / rating_count, 0) AS Rating
                  FROM catalog_book WHERE YEAR(added_at) = YEAR(NOW()) AND MONTH(added_at) = (MONTH(NOW()) - 1) ORDER BY ROUND(rating_stars / rating_count, 0) DESC LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Added at", "Status", "Rating"]

        elif misol == 8:
            with connection.cursor() as c:
                query = "SELECT id, name, content, added_at, updated_at, status " \
                        "FROM catalog_book WHERE added_at=updated_at LIMIT 10"
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Added at", "Updated at", "Status"]
        elif misol == 9:
            with connection.cursor() as c:
                query = "SELECT id, name, content, added_at, updated_at, status " \
                        "FROM catalog_book " \
                        "WHERE name NOT LIKE '%_____%' " \
                        "ORDER BY ROUND(rating_stars / rating_count) LIMIT 10"
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Added at", "Updated at", "Status"]
        elif misol == 10:
            with connection.cursor() as c:
                query = "SELECT id, name, content, added_at, publish_year, status " \
                        "FROM catalog_book WHERE publish_year IN(2010, 2015, 2020)  LIMIT 10"
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Added at", "Publish year", "Status"]
        elif misol == 11:
            with connection.cursor() as c:
                query = """SELECT id, name, content, added_at, publish_year, status 
                FROM catalog_book 
                WHERE publish_year IN(YEAR(NOW()), (YEAR(NOW()) - 1), (YEAR(NOW()) - 2))
                ORDER BY price DESC  LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Added at", "Publish year", "Status"]
        elif misol == 12:
            with connection.cursor() as c:
                query = """SELECT id, name, content, status, price, ROUND(rating_stars / rating_count, 0) AS rating
                  FROM catalog_book ORDER BY price DESC, ROUND(rating_stars / rating_count, 0) ASC LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Status", "Price", "Rating"]
        elif misol == 13:
            with connection.cursor() as c:
                query = """SELECT id, name, content, `read`, will_read, status 
                FROM catalog_book WHERE `read` > will_read"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Read", "Will read", "Status"]
        elif misol == 14:
            with connection.cursor() as c:
                query = """SELECT id, name, content, updated_at, status 
                FROM catalog_book 
                WHERE updated_at <> added_at ORDER BY updated_at DESC LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Updated at", "Status"]
        elif misol == 15:
            with connection.cursor() as c:
                query = """SELECT id, name, content, updated_at, status 
                FROM catalog_book WHERE name LIKE 'a%' LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Updated at", "Status"]
        elif misol == 16:
            with connection.cursor() as c:
                query = """SELECT id, name, content, updated_at, status 
                FROM catalog_book WHERE name LIKE 'de%' AND category_id IN(1,2,3)"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Updated at", "Status"]
        elif misol == 17:
            with connection.cursor() as c:
                query = """SELECT id, name, content, language_id, status, ROUND(rating_stars / rating_count, 0) AS rating 
                FROM catalog_book WHERE language_id IN(1,2)
                ORDER BY ROUND(rating_stars / rating_count, 0) DESC LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Language id", "Status", "Rating"]     
        elif misol == 18:
            with connection.cursor() as c:
                query = """SELECT id, name, content, country_id, language_id, status, ROUND(rating_stars / rating_count, 0) AS rating
                 FROM catalog_book WHERE country_id = 1 AND language_id <> 1
                ORDER BY ROUND(rating_stars / rating_count, 0) DESC LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Country id", "Language id", "Status", "Rating"]
        elif misol == 19:
            with connection.cursor() as c:
                query = """ SELECT id, name, content, avialability, language_id, status, ROUND(rating_stars / rating_count, 0) AS rating
                            FROM catalog_book WHERE name LIKE IN("a%", "r%", "s%") AND language_id <> 1 AND avialability IS FALSE
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Availability", "Language id", "Status", "Rating"]
        elif misol == 20:
            with connection.cursor() as c:
                query = """SELECT id, name, content, `read`, reading, will_read 
                 FROM catalog_book WHERE `read` = reading AND reading = will_read AND reading > 0"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Content", "Read", "Reading", "Will read"]
        elif misol == 21:
            with connection.cursor() as c:
                query = """SELECT cb.id, cb.name, cb.category_id, cb.price 
                        FROM 
                        (SELECT category_id, MIN(price) as m_price 
                        FROM catalog_book GROUP BY category_id) AS gb,
                        catalog_book AS cb
                        WHERE gb.m_price = cb.price AND gb.category_id = cb.category_id
                        ORDER BY price LIMIT 10"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Category id", "Price"]
        elif misol == 22:
            with connection.cursor() as c:
                query = """SELECT country_id, language_id, COUNT(*) AS soni
                        FROM catalog_book
                        GROUP BY country_id, language_id
                        ORDER BY soni"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Country ID", "Language ID", "Total books"]
        elif misol == 23:
            with connection.cursor() as c:
                query = """SELECT cb.id, cb.name, cb.read, cb.publish_year 
                        FROM 
                        (SELECT publish_year, MAX(`read`) as m_read 
                        FROM catalog_book WHERE publish_year >= YEAR(NOW()) - 10 
                        GROUP BY publish_year 
                        ORDER BY publish_year) AS gb,
                        catalog_book AS cb
                        WHERE gb.m_read = cb.read AND gb.publish_year = cb.publish_year
                        ORDER BY cb.publish_year"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Read", "Publish year"]
        elif misol == 24:
            with connection.cursor() as c:
                query = """SELECT cb.id, cb.name, ROUND(cb.rating_stars/cb.rating_count) as stars 
                        FROM (SELECT LEFT(name, 1) as name_alfa,
                        MAX(ROUND(rating_stars/rating_count)) AS r_stars
                        FROM catalog_book GROUP BY name_alfa) AS gb, catalog_book AS cb 
                        WHERE cb.name LIKE CONCAT(gb.name_alfa,'%') 
                        AND ROUND(cb.rating_stars/cb.rating_count) = gb.r_stars 
                        ORDER BY stars DESC"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["ID", "Name", "Stars"]
        elif misol == 25:
            with connection.cursor() as c:
                query = """SELECT LEFT(name, 1) as name_alfa, COUNT(*) 
                            FROM catalog_book 
                            GROUP BY name_alfa 
                            ORDER BY name_alfa"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Kitob nomining bosh harifi", "Soni"]
        elif misol == 26:
            with connection.cursor() as c:
                query = """SELECT status, COUNT(*)
                         FROM catalog_book 
                         GROUP BY status
                         ORDER BY status"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Statusi", "Soni"]
        elif misol == 27:
            with connection.cursor() as c:
                query = """SELECT YEAR(added_at) AS add_t, COUNT(*)
                         FROM catalog_book 
                         GROUP BY add_t
                         ORDER BY add_t"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Qo'shilgan yili", "Soni"]
        elif misol == 28:
            with connection.cursor() as c:
                query = """SELECT CASE WHEN ROUND(rating_stars / rating_count) > 4 AND
                            ROUND(rating_stars / rating_count) <= 5 THEN "4-5"
                        WHEN ROUND(rating_stars / rating_count) > 3 AND
                            ROUND(rating_stars / rating_count) <= 4 THEN "3-4"
                        WHEN ROUND(rating_stars / rating_count) > 2 AND
                            rating_stars / rating_count <= 3 THEN "2-3"
                        WHEN ROUND(rating_stars / rating_count) > 1 AND
                            rating_stars / rating_count <= 2 THEN "1-2"
                        ELSE "0-1" 
                        END AS count_st, COUNT(*)
                        FROM catalog_book GROUP BY count_st"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Reyting oraligi", "Soni"]
        elif misol == 29:
            with connection.cursor() as c:
                query = """SELECT MONTHNAME(added_at) AS add_t, COUNT(*) 
                            FROM catalog_book GROUP BY add_t"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Oy nomlari", "Soni"]
        elif misol == 30:
            with connection.cursor() as c:
                query = """SELECT CASE WHEN status = 0 AND avialability IS TRUE THEN "Yangi: Mavjud"
                        WHEN status = 0 AND avialability IS FALSE THEN "Yangi: Mavjud emas"
                        WHEN status = 1 AND avialability IS TRUE THEN "Qabul qilingan: Mavjud"
                        WHEN status = 1 AND avialability IS FALSE THEN "Qabul qilingan: Mavjud emas"
                        WHEN status = 2 AND avialability IS TRUE THEN "Bekor qilingan: Mavjud"
                        ELSE "Bekor qilingan: Mavjud emas"
                        END AS count_st, COUNT(*)
                        FROM catalog_book GROUP BY count_st"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Status", "Soni"]
        elif misol == 31:
            with connection.cursor() as c:
                query = """SELECT CASE WHEN price < 100000 THEN "Arzon"
                                WHEN price > 1000000 THEN "Qimmat"
                                ELSE "O'rta"
                            END AS count_st, COUNT(*)
                            FROM catalog_book GROUP BY count_st"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Narxlari", "Soni"]
        elif misol == 32:
            with connection.cursor() as c:
                query = """SELECT country_id, CASE WHEN price < 100000 THEN "Arzon"
                                WHEN price > 1000000 THEN "Qimmat"
                                ELSE "O'rta"
                            END AS count_st, COUNT(*)
                            FROM catalog_book GROUP BY country_id, count_st
                            ORDER BY country_id"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Davlatlar", "Narxlari", "Soni"]
        elif misol == 33:
            with connection.cursor() as c:
                query = """SELECT country_id, language_id, CASE WHEN price < 100000 THEN "Arzon"
                                WHEN price > 1000000 THEN "Qimmat"
                                ELSE "O'rta"
                            END AS count_st, COUNT(*)
                            FROM catalog_book GROUP BY country_id, language_id, count_st
                            ORDER BY country_id"""
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Davlatlar", "Kitob tillari", "Narxlari", "Soni"]
        elif misol == 34:
            with connection.cursor() as c:
                query = """ SELECT * FROM (SELECT "Eng arzon" as tp, name, min(price) as mp from catalog_book group by tp, name, price having mp <= 100000 order by price LIMIT 1) AS ha
                            UNION
                            SELECT * FROM (SELECT "O'rtacha eng arzon" as tp, name,  min(price) as mp from catalog_book group by tp, name, price having mp > 100000 and mp <= 1000000  order by price LIMIT 1) AS  hi
                            UNION
                            SELECT * FROM (SELECT "Qimmat eng arzon" as tp, name, min(price) as mp from catalog_book group by tp, name, price having mp > 1000000 order by price LIMIT 1) AS  hu 
                    """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Tarifi", "nomi", "Narxlari"]
        elif misol == 35:
            with connection.cursor() as c:
                query = """ SELECT CASE WHEN price < 100000 THEN "Arzon"
                                WHEN price > 1000000 THEN "Qimmat"
                                ELSE "O'rta"
                            END AS count_pt,
                             CASE WHEN ROUND(rating_stars / rating_count) > 4 AND
                                ROUND(rating_stars / rating_count) <= 5 THEN "4-5"
                            WHEN ROUND(rating_stars / rating_count) > 3 AND
                                ROUND(rating_stars / rating_count) <= 4 THEN "3-4"
                            WHEN ROUND(rating_stars / rating_count) > 2 AND
                                rating_stars / rating_count <= 3 THEN "2-3"
                            WHEN ROUND(rating_stars / rating_count) > 1 AND
                                rating_stars / rating_count <= 2 THEN "1-2"
                            ELSE "0-1" 
                            END AS count_rt, COUNT(*)
                            FROM catalog_book GROUP BY count_pt, count_rt
                            ORDER BY count_pt
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Narx bo'yicha", "Reting oralig'i", "Soni"]
        elif misol == 36:
            with connection.cursor() as c:
                query = """ SELECT name
                            FROM catalog_book GROUP BY name HAVING COUNT(name) > 1
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Nomi"]
        elif misol == 37:
            with connection.cursor() as c:
                query = """ SELECT publish_year, language_id, COUNT(*) as soni
                            FROM catalog_book 
                            GROUP BY publish_year, language_id ORDER BY soni DESC
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Chop etilgan yili", "Kitob tillari", "Soni"]
        elif misol == 38:
            with connection.cursor() as c:
                query = """ SELECT category_id, COUNT(*) as soni
                            FROM catalog_book 
                            WHERE rating_count = 0
                            GROUP BY category_id ORDER BY soni DESC
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Category id", "Soni"]
        elif misol == 39:
            with connection.cursor() as c:
                query = """ SELECT category_id, language_id, COUNT(*) as soni
                            FROM catalog_book 
                            WHERE rating_count = 0
                            GROUP BY category_id, language_id ORDER BY soni DESC
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Category id", "Language id", "Count"]
        elif misol == 40:
            with connection.cursor() as c:
                query = """ SELECT publish_year, COUNT(*) as soni
                            FROM catalog_book 
                            GROUP BY publish_year 
                            ORDER BY soni DESC
                            LIMIT 3
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Publish year", "Count"]
        elif misol == 41:
            with connection.cursor() as c:
                query = """ SELECT AVG(price)
                            FROM catalog_book 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Jami kitoblarning o'rtacha narxi"]
        elif misol == 42:
            with connection.cursor() as c:
                query = """ SELECT cc.name, COUNT(cb.name) FROM catalog_book as cb
                            INNER JOIN catalog_category as cc ON cc.id = cb.category_id
                            WHERE cc.name LIKE 'd%' 
                            GROUP BY cc.name 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Category name", "Total"]
        elif misol == 43:
            with connection.cursor() as c:
                query = """ SELECT cc.name, COUNT(cb.name) FROM catalog_book as cb
                            INNER JOIN catalog_language as cc ON cc.id = cb.language_id
                            GROUP BY cc.name 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["language name", "Total"]
        elif misol == 44:
            with connection.cursor() as c:
                query = """ SELECT ca.name, COUNT(cb.name) FROM catalog_book as cb
                            INNER JOIN catalog_book_authors as cba ON cba.book_id = cb.id
                            INNER JOIN catalog_author as ca ON ca.id = cba.author_id
                            WHERE ca.name LIKE '%a%'
                            GROUP BY ca.name 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Author name", "Total"]
        elif misol == 45:
            with connection.cursor() as c:
                query = """ SELECT avg(ROUND(rating_stars / rating_count)) FROM catalog_book
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Avarage rating"]
        elif misol == 46:
            with connection.cursor() as c:
                query = """ SELECT cc.name, 
                            AVG(ROUND(cb.rating_stars / cb.rating_count)) AS Ravg, 
                            MAX(ROUND(cb.rating_stars / cb.rating_count)) AS Rmax, 
                            MIN(ROUND(cb.rating_stars / cb.rating_count)) AS Rmin 
                            FROM catalog_book as cb
                            INNER JOIN catalog_category as cc ON cc.id = cb.category_id
                            GROUP BY cc.name 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Category name", "AVG rating", "MAX rating", "MIN rating"]
        elif misol == 47:
            with connection.cursor() as c:
                query = """ SELECT cl.name, 
                            SUM(cb.read) AS read_total, 
                            SUM(cb.reading) AS reading_total, 
                            SUM(cb.will_read) AS will_read_total 
                            FROM catalog_book as cb
                            INNER JOIN catalog_language as cl ON cl.id = cb.language_id
                            GROUP BY cl.name 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["language name", "Read total", "Reading total", "Will read total"]
        elif misol == 48:
            with connection.cursor() as c:
                query = """ SELECT ca.name, MAX(cb.publish_year), MIN(cb.publish_year) FROM catalog_book as cb
                            INNER JOIN catalog_book_authors as cba ON cba.book_id = cb.id
                            INNER JOIN catalog_author as ca ON ca.id = cba.author_id
                            GROUP BY ca.name 
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Author name", "Old Book year", "New Book year"]
        elif misol == 49:
            with connection.cursor() as c:
                query = """ SELECT cc.name, count(cb.id) FROM catalog_book as cb
                             INNER JOIN catalog_book_authors as cba ON cba.book_id = cb.id
                             INNER JOIN catalog_author as ca ON ca.id = cba.author_id
                             INNER JOIN catalog_category as cc ON cc.id = cb.category_id
                             GROUP BY cc.name, cb.id HAVING COUNT(cba.book_id) = 2
                        """
                c.execute(query)
                books = c.fetchall()
                sharti = savol[misol - 1]
                fields = ["Category name", "Total books"]
        elif misol == 50:
            with connection.cursor() as c:
                query = """ SELECT cc.name, AVG(cb.price) AS avg_bookp 
                            FROM catalog_book AS cb, 
                            (select id, name FROM catalog_category
                            where name like "F%") AS cc
                            WHERE cc.id = cb.category_id
                            GROUP BY cc.name
                        """
                c.execute(query)
                books = c.fetchall()
                print(books)
                sharti = savol[misol - 1]
                fields = ["Category name", "Avarage book price"]
    else:
        with connection.cursor() as c:
            query = "SELECT id, name, content, added_at, status FROM catalog_book ORDER BY id"
            c.execute(query)
            books = c.fetchall()
            sharti="Barcha kitoblar"
            fields = ["ID", "Name", "Content", "Added at", "Status"]

    return render(request, "table.html", context={
        "data": books,
        "txt": txt,
        "fields": fields,
        "misol_sharti": sharti
    })
    
