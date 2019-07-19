from rest_framework import serializers


class CinemaCityFilmSerializer(serializers.Serializer):
    name = serializers.CharField()
    length = serializers.IntegerField()
    release_year = serializers.IntegerField()
    cinema = serializers.CharField()
    date = serializers.DateTimeField()


class CinemaCityEventSerializer(serializers.Serializer):
    film = CinemaCityFilmSerializer()


class AddressInfoSerializer(serializers.Serializer):
    address_1 = serializers.CharField(source='address1', allow_null=True)
    address_2 = serializers.CharField(source='address2', allow_null=True)
    address_3 = serializers.CharField(source='address3', allow_null=True)
    address_4 = serializers.CharField(source='address4', allow_null=True)
    city = serializers.CharField()
    state = serializers.CharField(allow_null=True)
    postal_code = serializers.CharField(source='postalCode', allow_null=True)


class CinemaCityCinemaSerializer(serializers.Serializer):
    id = serializers.CharField()
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
    address_info = AddressInfoSerializer(source='addressInfo')
