from django.urls import path
from .views import MainIndexView, MainList, MainBookView, RegistrationView, LoginView, logout_view, UserInfoView, \
    MainSearchView

app_name = "catalog"

urlpatterns = [
    path("", MainIndexView.as_view(), name='index'),
    path("registration/", RegistrationView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("info/", UserInfoView.as_view(), name='userinfo'),
    path("logout/", logout_view, name='logout'),
    path("<str:slug>-<int:id>/", MainList.as_view(), name='list'),
    path("books/", MainList.as_view(), name='books'),
    path("<str:slug>-b<int:pk>/", MainBookView.as_view(), name='book'),
    path("search/", MainSearchView.as_view(), name='search'),

]
