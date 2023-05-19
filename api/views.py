import base64
import hashlib
import hmac
import json
import time

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView



from api.serializers import BookSerializer, BookEditSerializer, UserSerializer, LoginSerializer
from catalog.models import Book

class ApiBooks(APIView):

    def get(self, request):
        books = Book.objects.prefetch_related("category").order_by('id').all()
        data = BookSerializer(books, many=True)
        return Response(data.data)

    def post(self, request):
        data = BookEditSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        authors = data.validated_data.pop("authors")
        cuz, cru, cen  = data.validated_data.pop("content_uz"), data.validated_data.pop("content_ru"), data.validated_data.pop("content_en")
        book = Book(**data.validated_data)
        book.content_uz = json.dumps({"delta":"", "html": cuz})
        book.content_ru = json.dumps({"delta":"", "html": cru})
        book.content_en = json.dumps({"delta":"", "html": cen})
        book.save()
        book.authors.set(authors)

        return Response({
            "status": 'ok',
            "id": book.id
        })

class Me(APIView):
    permission_classes = []
    def get(self, request):

        return Response({
            "user": UserSerializer(request.user).data,
            "auth": request.auth
        })
    def post(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        user = authenticate(**data.validated_data)
        data = json.dumps({
            "user_id": str(user.id),
            "expire": time.time() + 30
        }).encode()
        sign = hmac.new(settings.SECRET_KEY.encode(), data, hashlib.sha256).hexdigest()
        data = base64.b64encode(data).decode()
        return Response({
            "token": f"{data}.{sign}"
        })
