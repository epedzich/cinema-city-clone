import datetime

from rest_framework import viewsets

from cinemas_repertoire.models import (
    AddressInfo,
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie,
)
from .serializers import (
    CinemaCityCinemaAPIResponseSerializer,
    CinemaCityCinemaModelSerializer,
    CinemaCityEventAPIResponseSerializer,
    CinemaCityEventModelSerializer,
    CinemaCityMovieAPIResponseSerializer,
    CinemaCityMovieModelSerializer,
)
from .utils import get_cinemas, get_film_events_response


class EventsViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityEventModelSerializer

    def get_queryset(self):
        update_events()
        return CinemaCityEvent.objects.all()


class CinemasViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityCinemaModelSerializer

    def get_queryset(self):
        update_cinemas()
        return CinemaCityCinema.objects.all()


class CCCinemasViewSet(CinemasViewSet):
    lookup_field = 'cc_cinema_id'


class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityMovieModelSerializer

    def get_queryset(self):
        update_movies()
        return CinemaCityMovie.objects.all()


def update_cinemas():
    cinema_list = []
    serializer = CinemaCityCinemaAPIResponseSerializer(get_cinemas().values(), many=True)
    for data in serializer.data:
        kwargs = data.copy()
        address_info_kwargs = kwargs.pop('address_info')
        cinema, _ = CinemaCityCinema.objects.update_or_create(cc_cinema_id=kwargs.pop('cc_cinema_id'), defaults=kwargs)
        if not cinema.address_info:
            address_info = AddressInfo.objects.create(**address_info_kwargs)
        else:
            address_info = cinema.address_info
        changed = False
        for key, value in address_info_kwargs.items():
            existing = getattr(address_info, key, None)
            if existing != value:
                setattr(address_info, key, value)
                changed = True
        if changed:
            address_info.save()

        if address_info.pk != cinema.address_info_id:
            cinema.address_info = address_info
            cinema.save()

        cinema_list.append(cinema)
    return serializer.data, cinema_list


def update_events(date=None):
    date = date or datetime.date.today()
    for cinema in get_cinemas(date=date).values():
        serializer = CinemaCityEventAPIResponseSerializer(get_film_events_response(cinema=cinema, date=date)['events'], many=True)
        for data in serializer.data:
            kwargs = data.copy()
            event, _ = CinemaCityEvent.objects.update_or_create(cc_event_id=kwargs.pop('cc_event_id'), defaults=kwargs)


def update_movies(date=None):
    date = date or datetime.date.today()
    for cinema in get_cinemas().values():
        serializer = CinemaCityMovieAPIResponseSerializer(get_film_events_response(cinema=cinema, date=date)['films'], many=True)
        for data in serializer.data:
            kwargs = data.copy()
            film, _ = CinemaCityMovie.objects.update_or_create(cc_movie_id=kwargs.pop('cc_movie_id'), defaults=kwargs)
