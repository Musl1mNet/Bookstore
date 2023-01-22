from django.urls import path
from .views import show_books
# from .views import
# registration, registration_send, show_users, show_file, book_add, book_add_send, show_books, show_category

app_name = "catalog"
urlpatterns = [
    path("", show_books, name='books'),
]

# path('', show_users, name='users'),
# path('user_<int:n>.txt', show_file, name='file'),
# path('registration/', registration, name='registration'),
# path('book-add/', book_add, name='Rbook'),
# path('book-data-send/', book_add_send, name='book-data-send'),
# path("data-send/", registration_send, name="user-data-send"),
# path('books/', show_books, name='books'),
# path('cotegory/', show_category, name='cotegory'),
