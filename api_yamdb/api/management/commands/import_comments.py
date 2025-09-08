import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review


User = get_user_model()


class Command(BaseCommand):
    help = "Импортирует комментарии."

    def handle(self, *args, **kwargs):
        with open('static/data/comments.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                review = get_object_or_404(Review, id=row['review_id'])
                author = get_object_or_404(User, id=row['author'])
                try:
                    Comment.objects.create(
                        id=row['id'],
                        review=review,
                        author=author,
                        text=row['text'],
                        pub_date=row['pub_date'],
                    )
                except IntegrityError as e:
                    print(f'Не удалось добавить комментарий по причине: {e}')
