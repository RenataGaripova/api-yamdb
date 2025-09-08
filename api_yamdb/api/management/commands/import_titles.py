import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from reviews.models import Category, Title


User = get_user_model()


class Command(BaseCommand):
    help = "Импортирует произведения."

    def handle(self, *args, **kwargs):
        with open('static/data/titles.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                category = get_object_or_404(
                    Category,
                    id=row['category']
                )
                try:
                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=category,
                    )
                except IntegrityError as e:
                    print(f'Не удалось добавить жанр по причине: {e}')
