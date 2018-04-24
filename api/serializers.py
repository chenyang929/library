from django.contrib.auth.models import User
from rest_framework import serializers
from storage.models import Storage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name')


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'book', 'inventory', 'remain')


class HistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    book = serializers.CharField()
    user = serializers.CharField()
    borrow_date = serializers.DateField()
    back_date = serializers.DateField()
    status = serializers.IntegerField()
    delay = serializers.IntegerField()
