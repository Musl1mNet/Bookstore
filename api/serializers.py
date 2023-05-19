from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils import json

from catalog.models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = ["id", "name", "category"]

class BookEditSerializer(serializers.ModelSerializer):
    photo = serializers.CharField(max_length=255)
    
    def save(self, **kwargs):
        data = self.validated_data.pop("data")
        authors = self.validated_data.pop("authors")
        cuz, cru, cen  = self.validated_data.pop("content_uz"), self.validated_data.pop("content_ru"), self.validated_data.pop("content_en")
        book = Book(**self.validated_data)
        book.content_uz = json.dumps({"delta":"", "html": cuz})
        book.content_ru = json.dumps({"delta":"", "html": cru})
        book.content_en = json.dumps({"delta":"", "html": cen})
        book = super().save(**kwargs)
        book.authors.set(authors)
        book.data = data

        return book
    
    class Meta:
        model = Book
        exclude = ["id", "added_at", "updated_at"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ["password"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
