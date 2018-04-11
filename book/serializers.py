from rest_framework import serializers
from .models import Book, History


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'book', 'inventory', 'remain', 'add_date')


class HistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    book = serializers.CharField()
    user = serializers.CharField()
    borrow_date = serializers.DateField()
    back_date = serializers.DateField()
    status = serializers.IntegerField()





