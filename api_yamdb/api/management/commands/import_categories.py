import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category

User = get_user_model()


class Command(BaseCommand):
    help = "Imports genres, categories and titles data from csv files."

    def handle(self, *args, **kwargs):
        with open('static/data/category.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    Category.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except IntegrityError as e:
                    print(f'Не удалось добавить жанр по причине: {e}')
