from django.urls import path
from .views import MainIndexView, MainList, MainBookView

app_name = "catalog"

urlpatterns = [
    path("", MainIndexView.as_view(), name='index'),
    path("<str:slug>-<int:id>/", MainList.as_view(), name='list'),
    path("books/", MainList.as_view(), name='books'),
    path("<str:slug>-b<int:pk>/", MainBookView.as_view(), name='book'),

]
