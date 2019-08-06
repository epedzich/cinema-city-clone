import datetime
import pytz

from rest_framework import serializers
from .models import (
    AddressInfo,
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie
)


class DateTimeFieldWihTZ(serializers.DateTimeField):
    """Class to make output of a DateTime Field timezone aware"""

    def to_representation(self, value):
        value_as_datetime = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        value = pytz.timezone('Europe/Warsaw').localize(value_as_datetime).astimezone(pytz.utc)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class UpdateIfExistsListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        ret = []
        for i, vd in zip(instance, validated_data):
            if i is None:
                ret.append(self.child.create(vd))
            else:
                ret.append(self.child.update(i, vd))
        return ret


class CinemaCityMovieAPIResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='cc_movie_id')
    name = serializers.CharField()
    length = serializers.IntegerField()
    posterLink = serializers.URLField(source='poster_link')
    videoLink = serializers.URLField(source='video_link')
    link = serializers.URLField()
    weight = serializers.IntegerField()
    releaseYear = serializers.IntegerField(source='release_year')
    attributeIds = serializers.ListField(source='attribute_ids')
    
    class Meta:
        list_serializer_class = UpdateIfExistsListSerializer
        model = CinemaCityMovie
        fields = [
            'id',
            'name',
            'length',
            'posterLink',
            'videoLink',
            'link',
            'weight',
            'releaseYear',
            'attributeIds'
        ]


class CinemaCityEventAPIResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='cc_event_id')
    filmId = serializers.CharField(source='cc_film_id')
    cinemaId = serializers.CharField(source='cc_cinema_id')
    businessDay = serializers.CharField(source='business_day')
    eventDateTime = DateTimeFieldWihTZ(source='event_datetime')
    attributeIds = serializers.ListField(source='attribute_ids')
    bookingLink = serializers.URLField(source='booking_link')
    soldOut = serializers.BooleanField(source='sold_out')

    class Meta:
        list_serializer_class = UpdateIfExistsListSerializer
        model = CinemaCityEvent
        fields = [
            'id',
            'filmId',
            'cinemaId',
            'businessDay',
            'eventDateTime',
            'attributeIds',
            'bookingLink',
            'soldOut',
        ]


class AddressInfoAPIResponseSerializer(serializers.Serializer):
    address_1 = serializers.CharField(source='address1', allow_null=True)
    address_2 = serializers.CharField(source='address2', allow_null=True)
    address_3 = serializers.CharField(source='address3', allow_null=True)
    address_4 = serializers.CharField(source='address4', allow_null=True)
    city = serializers.CharField()
    state = serializers.CharField(allow_null=True)
    postal_code = serializers.CharField(source='postalCode', allow_null=True)


class CinemaCityCinemaAPIResponseSerializer(serializers.Serializer):
    cc_cinema_id = serializers.CharField(source='id')
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


class CCAddressInfoAPIResponseSerializer(serializers.ModelSerializer):
    address1 = serializers.CharField(source='address_1', allow_null=True)
    address2 = serializers.CharField(source='address_2', allow_null=True)
    address3 = serializers.CharField(source='address_3', allow_null=True)
    address4 = serializers.CharField(source='address_4', allow_null=True)
    postalCode = serializers.CharField(source='postal_code', allow_null=True)

    class Meta:
        model = AddressInfo
        fields = ['address1', 'address2', 'address3', 'address4', 'city', 'state', 'postalCode']


class CCCinemaAPIResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='cc_cinema_id')
    groupId = serializers.CharField(source='group_id')
    displayName = serializers.CharField(source='display_name')
    link = serializers.URLField()
    imageUrl = serializers.URLField(source='image_url')
    address = serializers.CharField()
    bookingUrl = serializers.URLField(source='booking_url')
    blockOnlineSales = serializers.BooleanField(source='block_online_sales')
    blockOnlineSalesUntil = serializers.DateTimeField(source='block_online_sales_until', allow_null=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    addressInfo = CCAddressInfoAPIResponseSerializer(source='address_info')

    class Meta:
        list_serializer_class = UpdateIfExistsListSerializer
        model = CinemaCityCinema
        fields = [
            'id',
            'groupId',
            'displayName',
            'link',
            'imageUrl',
            'address',
            'bookingUrl',
            'blockOnlineSales',
            'blockOnlineSalesUntil',
            'latitude',
            'longitude',
            'addressInfo',
        ]

    def create(self, validated_data):
        validated_data = validated_data.copy()
        validated_data['address_info'] = AddressInfo.objects.create(**(validated_data.pop('address_info')))
        cinema = super().create(validated_data)
        return cinema

    def update(self, instance, validated_data):
        validated_data = validated_data.copy()
        address_info = instance.address_info
        changed = False
        for key, value in validated_data.pop('address_info').items():
            existing = getattr(address_info, key, None)
            if existing != value:
                setattr(address_info, key, value)
                changed = True
        if changed:
            address_info.save()
        return super().update(instance, validated_data)


class AddressInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInfo
        fields = ['address_1', 'address_2', 'address_3', 'address_4', 'city', 'state', 'postal_code']


class CinemaCityCinemaModelSerializer(serializers.ModelSerializer):
    address_info = AddressInfoModelSerializer()
    detail_link = serializers.HyperlinkedIdentityField(view_name='cinemas-detail')

    class Meta:
        model = CinemaCityCinema
        fields = [
            'id', 'detail_link', 'cc_cinema_id', 'group_id', 'display_name', 'link', 'image_url', 'address',
            'booking_url', 'block_online_sales', 'block_online_sales_until', 'latitude', 'longitude', 'address_info'
        ]


class CinemaCityMovieModelSerializer(serializers.ModelSerializer):
    detail_link = serializers.HyperlinkedIdentityField(view_name='movies-detail')

    class Meta:
        model = CinemaCityMovie
        fields = [
            'id', 'detail_link', 'cc_movie_id', 'name', 'length', 'poster_link', 'video_link', 'link', 'weight',
            'release_year', 'attribute_ids'
        ]


class CinemaCityEventModelSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='events-detail')
    cc_cinema = serializers.HyperlinkedRelatedField(
        lookup_field='cc_cinema_id',
        view_name='cc-cinemas-detail',
        read_only=True
    )

    class Meta:
        model = CinemaCityEvent
        fields = [
            'id', 'link', 'cc_event_id', 'cc_film_id', 'cc_cinema_id', 'business_day', 'event_datetime',
            'attribute_ids', 'booking_link', 'sold_out', 'cc_cinema'
        ]
