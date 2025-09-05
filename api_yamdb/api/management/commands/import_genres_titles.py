import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Genre, Title

User = get_user_model()


class Command(BaseCommand):
    help = "Imports genres, categories and titles data from csv files."

    def handle(self, *args, **kwargs):
        with open('static/data/genre_title.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = get_object_or_404(Title, id=row['title_id'])
                genre_add = get_object_or_404(
                    Genre,
                    id=row['genre_id']
                )
                title.genre.add(genre_add)
