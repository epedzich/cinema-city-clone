from django.contrib.postgres.fields import ArrayField
from django.db import models


class AddressInfo(models.Model):
    address_1 = models.CharField(max_length=100, null=True)
    address_2 = models.CharField(max_length=100, null=True)
    address_3 = models.CharField(max_length=100, null=True)
    address_4 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50,)
    state = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=10, null=True)


class CinemaCityCinema(models.Model):
    cc_cinema_id = models.CharField(max_length=10, unique=True)
    group_id = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100)
    link = models.URLField()
    image_url = models.URLField()
    address = models.CharField(max_length=100)
    booking_url = models.URLField()
    block_online_sales = models.BooleanField()
    block_online_sales_until = models.DateTimeField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address_info = models.OneToOneField(AddressInfo, on_delete=models.CASCADE, null=True, blank=True)


class CinemaCityMovie(models.Model):
    cc_movie_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    length = models.IntegerField()
    poster_link = models.URLField()
    video_link = models.URLField()
    link = models.URLField()
    weight = models.IntegerField()
    release_year = models.IntegerField()
    attribute_ids = ArrayField(models.CharField(max_length=10))


class CinemaCityEvent(models.Model):
    cc_event_id = models.CharField(max_length=10, unique=True)
    cc_film = models.ForeignKey(CinemaCityMovie, on_delete=models.CASCADE, to_field='cc_movie_id', db_constraint=False)
    cc_cinema = models.ForeignKey(CinemaCityCinema, on_delete=models.CASCADE, to_field='cc_cinema_id', db_constraint=False)
    business_day = models.CharField(max_length=15)
    event_datetime = models.DateTimeField()
    attribute_ids = ArrayField(models.CharField(max_length=10))
    booking_link = models.URLField()
    sold_out = models.BooleanField()
