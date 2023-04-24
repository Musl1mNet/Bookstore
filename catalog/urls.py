from django.urls import path
from .views import MainIndexView

app_name = "catalog"

urlpatterns = [
    path("", MainIndexView.as_view(), name='home'),
    ]
