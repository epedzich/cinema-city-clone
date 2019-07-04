import datetime

import requests


cinemas_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/cinemas/with-event/until/2020-06-20'
movies_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events/in-cinema/1067/at-date/2019-06-21'
events_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events-dates/in-cinema/1067/as-at-date/2019-06-21'
trailers_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/10103/trailers/byCinemaId/1067'

quickbook_url = 'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103'


def get_cinemas(date=datetime.date.today()):
    response = requests.get(
        f'{quickbook_url}/cinemas/with-event/until/{date}')
    response.raise_for_status()
    return {
        cinema['id']: cinema
        for cinema in response.json()['body']['cinemas']
    }


def get_movies(cinema, date=datetime.date.today()):
    response = requests.get(f'{quickbook_url}/film-events/in-cinema/{cinema["id"]}/at-date/{date}')
    response.raise_for_status()

    movies_response = response.json()['body']

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
    response = requests.get(f'{quickbook_url}/dates/in-cinema/{cinema_id}/until/2020-06-30')
    response.raise_for_status()

    dates_response = response.json()['body']['dates']
    return dates_response
