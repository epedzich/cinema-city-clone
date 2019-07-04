import datetime

from django import forms
from django.forms.widgets import ChoiceWidget

from .utils import get_cinemas, get_dates

CINEMA_CHOICES = [(cinema['id'], cinema['displayName']) for cinema in get_cinemas().values()]


class CinemaForm(forms.Form):
    cinema_id = forms.ChoiceField(choices=CINEMA_CHOICES, label='', initial=CINEMA_CHOICES[0][0])


class DateSubmitField(ChoiceWidget):
    input_type = 'submit'
    template_name = 'django/forms/widgets/multiple_input.html'
    option_template_name = 'cinemas_repertoire/submit_choice.html'

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        ret = super(DateSubmitField, self).create_option(
            name, value, label, selected, index,
            subindex=subindex, attrs=attrs)

        classes = set(ret['attrs'].get('class', '').split(' '))
        classes |= {'btn', 'btn-info', 'btn-sm'}
        if selected:
            classes.discard('btn-info')
            classes.add('btn-light')

        ret['attrs']['class'] = ' '.join(classes)
        return ret


class DateChoiceField(forms.ChoiceField):
    widget = DateSubmitField

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class DateForm(forms.Form):
    date = DateChoiceField(label='')

    def set_cinema_id(self, cinema_id):
        def get_date_choice(date_value):
            date_display = datetime.datetime.strptime(date_value, '%Y-%m-%d').strftime('%a %d.%m')
            return date_value, date_display

        self.fields['date'].choices = list(map(get_date_choice, get_dates(cinema_id)))
