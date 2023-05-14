from django.urls import path

from api.views import ApiBooks

app_name = 'api'
urlpatterns = [
    path('books/', ApiBooks.as_view(), name="books")
]