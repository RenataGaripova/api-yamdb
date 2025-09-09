import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = "Импортирует пользователей."

    def handle(self, *args, **kwargs):
        with open('static/data/users.csv', mode='r') as file:
            objects_to_create = []
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                objects_to_create.append(
                    User(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                )

            User.objects.bulk_create(objects_to_create)
