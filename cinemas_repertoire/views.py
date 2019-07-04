import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

from .utils import get_cinemas, get_movies, get_dates
from .forms import CinemaForm, DateForm


def cinema_dates(request, cinema_id):
    response = HttpResponse(json.dumps(get_dates(cinema_id)))
    response['Content-Type'] = 'application/json'
    return response


def events_list(request):
    form_data = request.GET.copy()
    cinema_id = request.session.get('cinema_id')
    if cinema_id:
        form_data.setdefault('cinema_id', cinema_id)

    form_data.setdefault('date', str(datetime.date.today()))
    form_data.setdefault('cinema_id', '1088')

    cinema_form = CinemaForm(form_data or None)
    date_form = DateForm(form_data)

    date = ''
    events = []
    if cinema_form.is_valid():
        cinema_id = cinema_form.cleaned_data['cinema_id']
        date_form.set_cinema_id(cinema_id)
        if date_form.is_valid():
            date = date_form.cleaned_data['date']
            events = get_movies(get_cinemas()[cinema_id], date=date)
            request.session['cinema_id'] = cinema_id

    return render(request, template_name='cinemas_repertoire/cinemas_list.html', context={
        "cinema_form": cinema_form,
        "date_form": date_form,
        "events": events,
        "date": date,
    })
