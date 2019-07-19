from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CinemaCityCinemaSerializer, CinemaCityFilmSerializer
from .utils import get_cinemas, get_movies, get_movie_details


class EventsViewset(viewsets.ViewSet):

    def list(self, request):
        movie_data = [
            {
                "cinema": cinema['id'],
                "date": event['eventDateTime'],
                "name": event['film']['name'],
                "length": event['film']['length'],
                "release_year": event['film']['releaseYear'],
            }
            for cinema in get_cinemas().values()
            for event in get_movies(cinema).values()
        ]
        results = CinemaCityFilmSerializer(movie_data, many=True).data
        return Response(results)


class CinemasViewset(viewsets.ViewSet):

    def list(self, request):
        movie_data = list(get_cinemas().values())
        results = CinemaCityCinemaSerializer(movie_data, many=True).data
        return Response(results)