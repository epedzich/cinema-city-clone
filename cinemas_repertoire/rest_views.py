from rest_framework import viewsets
from rest_framework.response import Response

from cinemas_repertoire.models import (
    AddressInfo,
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie,
)
from .serializers import (
    CinemaCityCinemaAPIResponseSerializer,
    CinemaCityEventAPIResponseSerializer,
    CinemaCityMovieAPIResponseSerializer,
    CinemaCityCinemaModelSerializer,
    CinemaCityEventModelSerializer,
    CinemaCityMovieModelSerializer,
)
from .utils import get_cinemas, get_movies


class EventsViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityEventModelSerializer

    def get_queryset(self):
        update_events()
        return CinemaCityEvent.objects.all()

    # def list(self, request):
    #     movie_data = [
    #         {
    #             "cinema": cinema['id'],
    #             "date": event['eventDateTime'],
    #             "name": event['film']['name'],
    #             "length": event['film']['length'],
    #             "release_year": event['film']['releaseYear'],
    #         }
    #         for cinema in get_cinemas().values()
    #         for event in get_movies(cinema).values()
    #     ]
    #     results = CinemaCityMovieAPIResponseSerializer(movie_data, many=True).data
    #     return Response(results)


class CinemasViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityCinemaModelSerializer

    def get_queryset(self):
        update_cinemas()
        return CinemaCityCinema.objects.all()


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
        cinema, _ = CinemaCityCinema.objects.update_or_create(cinema_id=kwargs.pop('cinema_id'), defaults=kwargs)
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


def update_events():
    pass


def update_movies():
    pass
