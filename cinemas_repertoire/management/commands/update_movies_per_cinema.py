from django.core.management.base import BaseCommand, CommandError
from cinemas_repertoire import tasks


class Command(BaseCommand):
    help = 'Runs celery task update_movies_per_cinema'

    def add_arguments(self, parser):
        parser.add_argument('cinema_id', type=str)

    def handle(self, *args, **options):
        tasks.update_movies_per_cinema(cinema_id=options['cinema_id'])
