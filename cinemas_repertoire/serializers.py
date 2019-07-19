from rest_framework import serializers
from .models import (
    AddressInfo,
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie
)


class CinemaCityMovieAPIResponseSerializer(serializers.Serializer):
    movie_id = serializers.CharField(source='id')
    name = serializers.CharField()
    length = serializers.IntegerField()
    poster_link = serializers.URLField(source='posterLink')
    video_link = serializers.URLField(source='videoLink')
    link = serializers.URLField()
    weight = serializers.IntegerField()
    release_year = serializers.IntegerField()
    attribute_ids = serializers.ListField(source='attributeIds')


class CinemaCityEventAPIResponseSerializer(serializers.Serializer):
    event_id = serializers.CharField(source='id')
    film_id = serializers.CharField(source='filmId')
    cinema_id = serializers.CharField(source='cinemaId')
    business_day = serializers.CharField(source='businessDay')
    event_datetime = serializers.DateTimeField(source='eventDateTime')
    attribute_ids = serializers.ListField(source='attributeIds')
    booking_link = serializers.URLField(source='bookingLink')
    sold_out = serializers.BooleanField(source='soldOut')


class AddressInfoAPIResponseSerializer(serializers.Serializer):
    address_1 = serializers.CharField(source='address1', allow_null=True)
    address_2 = serializers.CharField(source='address2', allow_null=True)
    address_3 = serializers.CharField(source='address3', allow_null=True)
    address_4 = serializers.CharField(source='address4', allow_null=True)
    city = serializers.CharField()
    state = serializers.CharField(allow_null=True)
    postal_code = serializers.CharField(source='postalCode', allow_null=True)


class CinemaCityCinemaAPIResponseSerializer(serializers.Serializer):
    cinema_id = serializers.CharField(source='id')
    group_id = serializers.CharField(source='groupId')
    display_name = serializers.CharField(source='displayName')
    link = serializers.URLField()
    image_url = serializers.URLField(source='imageUrl')
    address = serializers.CharField()
    booking_url = serializers.URLField(source='bookingUrl')
    block_online_sales = serializers.BooleanField(source='blockOnlineSales')
    block_online_sales_until = serializers.DateTimeField(source='blockOnlineSalesUntil', allow_null=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    address_info = AddressInfoAPIResponseSerializer(source='addressInfo')


class AddressInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInfo
        fields = ['address_1', 'address_2', ' address_3', 'address_4', 'city', 'state', 'postal_code']


class CinemaCityCinemaModelSerializer(serializers.ModelSerializer):
    address_info = AddressInfoModelSerializer()

    class Meta:
        model = CinemaCityCinema
        fields = [
            'id', 'group_id', 'display_name', 'link', 'image_url', 'address', 'booking_url', 'block_online_sales',
                  'block_online_sales_until', 'latitude', 'longitude', 'address_info'
        ]


class CinemaCityMovieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaCityMovie
        fields = [
            'movie_id', 'name', 'length', 'poster_link', 'video_link', 'link', 'weight', 'release_year', 'attribute_ids'
        ]


class CinemaCityEventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaCityEvent
        fields = [
            'event_id', 'film', 'cinema', 'business_day', 'event_datetime', 'attribute_ids', 'booking_link', 'sold_out'
        ]
