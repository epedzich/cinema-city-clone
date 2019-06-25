import datetime

import requests
from flask import Flask
from jinja2 import Template

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

    return events


app = Flask(__name__)

with open('get_events.j2') as f:
    template = Template(f.read())


@app.route('/')
def get_events():
    cinema_id = '1067'
    date = datetime.date.today()

    cinemas = get_cinemas(date=date)
    events = get_movies(cinemas[cinema_id], date=date)

    return template.render(events=events, date=date)
