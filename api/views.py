from rest_framework.response import Response
from rest_framework.views import APIView



from api.serializers import BookSerializer
from catalog.models import Book

class ApiBooks(APIView):

    def get(self, request):
        books = Book.objects.prefetch_related("category").order_by('id').all()
        data = BookSerializer(books, many=True)
        return Response(data.data)
