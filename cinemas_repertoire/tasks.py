from __future__ import absolute_import, unicode_literals

import datetime

from celery.schedules import crontab
from requests import RequestException

from cinema_city_clone.celery import app
from cinemas_repertoire.models import (
    AddressInfo,
    CinemaCityCinema,
    CinemaCityEvent,
    CinemaCityMovie
)
from cinemas_repertoire.serializers import (
    CinemaCityCinemaAPIResponseSerializer,
    CinemaCityEventAPIResponseSerializer,
    CinemaCityMovieAPIResponseSerializer
)
from cinemas_repertoire.utils import get_cinemas, get_film_events_response, get_dates


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
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
    return [cinema.cc_cinema_id for cinema in cinema_list]


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def update_events_per_cinema(cinema_id, date=None):
    date = date or datetime.date.today()
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    cinema = get_cinemas()[cinema_id]
    serializer = CinemaCityEventAPIResponseSerializer(get_film_events_response(cinema=cinema, date=date)['events'],
                                                      many=True)
    for data in serializer.data:
        kwargs = data.copy()
        event, _ = CinemaCityEvent.objects.update_or_create(cc_event_id=kwargs.pop('cc_event_id'), defaults=kwargs)


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def update_movies_per_cinema(cinema_id, date=None):
    date = date or datetime.date.today()
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    cinema = get_cinemas()[cinema_id]
    serializer = CinemaCityMovieAPIResponseSerializer(get_film_events_response(cinema=cinema, date=date)['films'],
                                                      many=True)
    for data in serializer.data:
        kwargs = data.copy()
        film, _ = CinemaCityMovie.objects.update_or_create(cc_movie_id=kwargs.pop('cc_movie_id'), defaults=kwargs)


@app.task()
def update_events_and_movies(cinema_ids):
    for cinema_id in cinema_ids:
        dates = get_dates(cinema_id=cinema_id)
        for date in dates:
            update_events_per_cinema.delay(cinema_id, date)
        update_movies_per_cinema.delay(cinema_id)


@app.task()
def update_cinemas_events_and_movies():
    update_cinemas.apply_async((), link=update_events_and_movies.s())


app.conf.beat_schedule = {
    'update_from_api_once_a_day': {
        'task': 'cinemas_repertoire.tasks.update_cinemas_events_and_movies',
        'schedule': crontab(minute=0, hour=0)
    }
}

