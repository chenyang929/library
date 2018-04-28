from django.contrib.auth.models import User
from rest_framework import serializers
from storage.models import Storage
from history.models import History


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name')


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'book', 'inventory', 'remain')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('id', 'book', 'user', 'status', 'delay', 'borrow_date', 'back_date')
