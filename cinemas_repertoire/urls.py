from django.urls import path
from . import views

app_name = "repertoire"

urlpatterns = [
    path('', views.events_list, name='cinema_movies'),
    path('cinema-dates/<str:cinema_id>', views.cinema_dates, name='cinema_dates'),
    path('event/<slug:id>', views.event_detail, name='event_detail'),
]
