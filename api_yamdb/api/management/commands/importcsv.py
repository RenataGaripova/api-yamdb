import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    help = "Imports data from csv files."

    def handle(self, *args, **kwargs):
        csv_files = (
            os.path.join(settings.BASE_DIR, 'static/data/category.csv'),
            os.path.join(settings.BASE_DIR, 'static/data/genre.csv'),
            os.path.join(settings.BASE_DIR, 'static/data/titles.csv'),
        )

        for csv_file in csv_files:
            with open(csv_file, mode='r') as file:
                objects_to_create = []
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if csv_file.endswith("category.csv"):
                        objects_to_create.append(
                            Category(name=row['name'], slug=row['slug'],)
                        )
                    elif csv_file.endswith("genre.csv"):
                        objects_to_create.append(
                            Genre(name=row['name'], slug=row['slug'],)
                        )
                    elif csv_file.endswith("titles.csv"):
                        category = Category.objects.get(pk=row['category'])
                        objects_to_create.append(
                            Title(
                                name=row['name'],
                                year=row['year'],
                                category=category,
                            )
                        )

                if 'category' in csv_file:
                    Category.objects.bulk_create(objects_to_create)
                elif 'genre' in csv_file:
                    Genre.objects.bulk_create(objects_to_create)
                elif 'title' in csv_file:
                    Title.objects.bulk_create(objects_to_create)
