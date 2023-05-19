from django.urls import path
from rest_framework.authtoken import views
from api.views import ApiBooks, Me

app_name = 'api'
urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('books/', ApiBooks.as_view(), name="books"),
    path('me/', Me.as_view(), name="me"),
]