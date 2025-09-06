import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from reviews.models import Title, Review

User = get_user_model()


class Command(BaseCommand):
    help = "Импортирует отзывы."

    def handle(self, *args, **kwargs):
        with open('static/data/review.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = get_object_or_404(Title, id=row['title_id'])
                author = get_object_or_404(User, id=row['author'])
                try:
                    Review.objects.create(
                        id=row['id'],
                        title=title,
                        author=author,
                        text=row['text'],
                        pub_date=row['pub_date'],
                        score=row['score'],
                    )
                except IntegrityError as e:
                    print(f'Не удалось добавить отзыв по причине: {e}')
