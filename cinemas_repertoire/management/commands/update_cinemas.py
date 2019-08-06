from django.core.management.base import BaseCommand, CommandError
from cinemas_repertoire import tasks


class Command(BaseCommand):
    help = 'Runs celery task update_cinemas'

    def handle(self, *args, **options):
        tasks.update_cinemas()
