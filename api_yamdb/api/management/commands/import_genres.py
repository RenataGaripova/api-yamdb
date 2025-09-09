import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Genre


User = get_user_model()


class Command(BaseCommand):
    help = "Импортирует жанры."

    def handle(self, *args, **kwargs):
        with open('static/data/genre.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except IntegrityError as e:
                    print(f'Не удалось добавить жанр по причине: {e}')
