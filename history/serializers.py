from rest_framework import serializers


class HistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    book = serializers.CharField()
    user = serializers.CharField()
    borrow_date = serializers.DateField()
    back_date = serializers.DateField()
    status = serializers.IntegerField()
