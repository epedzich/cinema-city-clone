from rest_framework import serializers


class FilmSerializer(serializers.Serializer):
    name = serializers.CharField()
    length = serializers.IntegerField()
    release_year = serializers.IntegerField()
    cinema = serializers.CharField()
    date = serializers.DateTimeField()
