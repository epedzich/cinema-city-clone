import datetime

from django.core.cache import cache

import requests

cinemas_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/cinemas/with-event/until/2020-06-20'
movies_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events/in-cinema/1067/at-date/2019-06-21'
events_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events-dates/in-cinema/1067/as-at-date/2019-06-21'
trailers_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/10103/trailers/byCinemaId/1067'
movie_details_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/films/until/2020-07-04?attr=&lang=pl_PL'

quickbook_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103'


def get_cached_response(url):
    def get_response():
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    return cache.get_or_set(url, get_response)


def get_cinemas(date=None):
    date = date or (datetime.date.today() + datetime.timedelta(days=30))
    api_response = get_cached_response(url=f'{quickbook_url}/cinemas/with-event/until/{date}')
    return {
        cinema['id']: cinema
        for cinema in api_response['body']['cinemas']
    }


def get_film_events_response(cinema, date=None):
    date = date or datetime.date.today()
    api_response = get_cached_response(url=f'{quickbook_url}/film-events/in-cinema/{cinema["id"]}/at-date/{date}')
    return api_response['body']


def get_dates(cinema_id):
    api_response = get_cached_response(url=f'{quickbook_url}/dates/in-cinema/{cinema_id}/until/2020-06-30')
    return api_response['body']['dates']

