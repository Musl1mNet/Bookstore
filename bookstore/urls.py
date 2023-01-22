"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter, include
from django.http.response import HttpResponse
from datetime import datetime

class DateConverter:
    regex = 'bd-([0-9]{4})-([0-9]{2})-([0-9]{2})'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
register_converter(DateConverter, "date")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("salom/", lambda request: HttpResponse(f"{request.GET.get('q')[::-1]}")),
    path('diff/<date:q>', lambda request, q: HttpResponse(f"Hozirgi vaqtdan {int((datetime.now() - datetime.strptime(q, 'bd-%Y-%m-%d')).days) // 365} yil {(int((datetime.now() - datetime.strptime(q, 'bd-%Y-%m-%d')).days) % 365) // 30} oy {(int((datetime.now() - datetime.strptime(q, 'bd-%Y-%m-%d')).days) % 365) % 30} kun farqli!")),
    path('', include('catalog.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
