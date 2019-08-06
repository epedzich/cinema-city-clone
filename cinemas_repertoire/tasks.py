from __future__ import absolute_import, unicode_literals

import datetime

from cinema_city_clone import settings
from requests import RequestException

from cinema_city_clone.celery import app
from cinemas_repertoire.models import (
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie
)
from cinemas_repertoire.serializers import (
    CCCinemaAPIResponseSerializer,
    CinemaCityEventAPIResponseSerializer,
    CinemaCityMovieAPIResponseSerializer
)
from cinemas_repertoire.utils import get_cinemas, get_film_events_response, get_dates


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def update_cinemas():
    responses = list(get_cinemas().values())
    instances = {
        cinema.cc_cinema_id: cinema
        for cinema in CinemaCityCinema.objects.filter(cc_cinema_id__in=[r['id'] for r in responses])
    }
    instances = [instances.get(r['id'], None) for r in responses]
    serializer = CCCinemaAPIResponseSerializer(instances, data=responses, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    ret = [cinema.cc_cinema_id for cinema in serializer.instance]
    return ret


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def update_events_per_cinema(cinema_id, date=None):
    date = date or datetime.date.today()
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    cinema = get_cinemas()[cinema_id]
    responses = get_film_events_response(cinema=cinema, date=date)['events']
    instances = {
        event.cc_event_id: event
        for event in CinemaCityEvent.objects.filter(cc_event_id__in=[r['id'] for r in responses])
    }
    instances = [instances.get(r['id'], None) for r in responses]
    serializer = CinemaCityEventAPIResponseSerializer(instances, data=responses, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def update_movies_per_cinema(cinema_id, date=None):
    date = date or datetime.date.today()
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    cinema = get_cinemas()[cinema_id]
    responses = get_film_events_response(cinema=cinema, date=date)['films']
    instances = {
        movie.cc_movie_id: movie
        for movie in CinemaCityMovie.objects.filter(cc_movie_id__in=[r['id'] for r in responses])
    }
    instances = [instances.get(r['id'], None) for r in responses]
    serializer = CinemaCityMovieAPIResponseSerializer(instances, data=responses, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@app.task()
def update_events_and_movies(cinema_ids):
    for cinema_id in cinema_ids:
        dates = get_dates(cinema_id=cinema_id)
        for date in dates:
            update_events_per_cinema.delay(cinema_id, date)
            update_movies_per_cinema.delay(cinema_id, date)


@app.task()
def update_cinemas_events_and_movies():
    update_cinemas.apply_async((), link=update_events_and_movies.s())


app.conf.beat_schedule = {
    'update_from_api_at_midnight': {
        'task': 'cinemas_repertoire.tasks.update_cinemas_events_and_movies',
        'schedule': settings.CRON_UPDATE_FROM_API_AT_MIDNIGHT
    }
}
