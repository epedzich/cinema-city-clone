from rest_framework import viewsets

from cinemas_repertoire.models import (
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie,
)
from .serializers import (
    CinemaCityCinemaModelSerializer,
    CinemaCityEventModelSerializer,
    CinemaCityMovieModelSerializer,
)


class EventsViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityEventModelSerializer

    def get_queryset(self):
        return CinemaCityEvent.objects.all()


class CinemasViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityCinemaModelSerializer

    def get_queryset(self):
        return CinemaCityCinema.objects.all()


class CCCinemasViewSet(CinemasViewSet):
    lookup_field = 'cc_cinema_id'


class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaCityMovieModelSerializer

    def get_queryset(self):
        return CinemaCityMovie.objects.all()
