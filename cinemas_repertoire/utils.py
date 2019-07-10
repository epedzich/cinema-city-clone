import datetime

from django.core.cache import cache

import requests

cinemas_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/cinemas/with-event/until/2020-06-20'
movies_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events/in-cinema/1067/at-date/2019-06-21'
events_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events-dates/in-cinema/1067/as-at-date/2019-06-21'
trailers_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/10103/trailers/byCinemaId/1067'
movie_details_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/films/until/2020-07-04?attr=&lang=pl_PL'

quickbook_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103'


def get_cinemas(date=datetime.date.today()):
    def get_response():
        response = requests.get(
            f'{quickbook_url}/cinemas/with-event/until/{date}')
        response.raise_for_status()
        return response.json()
    api_response = cache.get_or_set('api_get_cinemas', get_response)
    return {
        cinema['id']: cinema
        for cinema in api_response['body']['cinemas']
    }


def get_movies(cinema, date=datetime.date.today()):
    def get_response():
        response = requests.get(f'{quickbook_url}/film-events/in-cinema/{cinema["id"]}/at-date/{date}')
        response.raise_for_status()
        return response.json()
    api_response = cache.get_or_set('api_get_movies', get_response)
    movies_response = api_response['body']

    films = {
        film['id']: film
        for film in movies_response['films']
    }
    events = {
        event['id']: event
        for event in movies_response['events']
    }

    for event in events.values():
        film_id = event['filmId']
        event['cinema'] = cinema
        event['film'] = films[film_id]
        event['day'], event['hour'] = event['eventDateTime'].split('T')
        event['hour'] = event['hour'][:5]
        event_attributes = event['attributeIds']
        event['attributes'] = ', '.join([attr for attr in event_attributes if attr in '2d 3d imax 4dx dubbed subbed'])

    return events


def get_dates(cinema_id):
    def get_response():
        response = requests.get(f'{quickbook_url}/dates/in-cinema/{cinema_id}/until/2020-06-30')
        response.raise_for_status()
        return response.json()
    api_response = cache.get_or_set('api_get_dates', get_response)
    dates_response = api_response['body']['dates']
    return dates_response


def get_movie_details(film_id):
    def get_response():
        response = requests.get(f'{quickbook_url}/films/until/{datetime.date.today()}')
        response.raise_for_status()
        return response.json()
    api_response = cache.get_or_set('api_get_movie_details', get_response)
    films_list = api_response['body']['films']
    return next(film for film in films_list if film['id'] == film_id)
