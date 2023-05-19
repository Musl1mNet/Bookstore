from django.contrib.auth.models import User
from rest_framework import serializers

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
