from datetime import datetime
import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView

from .forms import CinemaForm, DateForm
from .models import CinemaCityEvent, CinemaCityMovie
from .utils import get_dates


def cinema_dates(request, cinema_id):
    response = HttpResponse(json.dumps(get_dates(cinema_id)))
    response['Content-Type'] = 'application/json'
    return response


def events_list(request):
    form_data = request.GET.copy()
    cinema_id = request.session.get('cinema_id')
    if cinema_id:
        form_data.setdefault('cinema_id', cinema_id)

    form_data.setdefault('date', str(datetime.today().date()))
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
            if date == datetime.today().date():
                date_time_now = datetime.combine(date, timezone.now().timetz())
            else:
                date_time_now = timezone.make_aware(datetime.combine(date, datetime.min.time()))
            date_time_eod = timezone.make_aware(datetime.combine(date, datetime.max.time()))
            events = CinemaCityEvent.objects.filter(
                Q(cc_cinema=cinema_id, event_datetime__range=[date_time_now, date_time_eod]))
            request.session['cinema_id'] = cinema_id

    return render(request, template_name='cinemas_repertoire/cinemas_list.html', context={
        "cinema_form": cinema_form,
        "date_form": date_form,
        "events": events,
        "date": date,
    })


class FilmDetailView(DetailView):
    model = CinemaCityMovie
    template_name = 'cinemas_repertoire/film_detail.html'
    context_object_name = 'film'
    slug_field = 'cc_movie_id'
