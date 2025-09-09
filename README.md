# api_yamdb
# API для Yatube.
API для приложения YaMDb на Django Rest Framework, разработанное в рамках курса Python разработчик.
#### Модели Yatube:
*   Модели произведений, категорий, жанров, отзывов и комментариев хранятся в приложении reviews проекта api_yamdb.
*   В приложении users реализована работа с кастомным пользователем и ролями пользователей.
*   Category - модель категорий произведений. Каждое произведение относится к одной категории. Добавлять категории может только админ.
*   Genre - модель жанров произведений. У одного произведения может быть множество жанров. Добавлять жанры может только админ.
*   Title - модель произведения. Произведением может быть определённый фильм, книга или песня. Добавлять произведения может только админ.
*   Review - модель отзывов. Отзыв привязан к определённому произведению. Публиковать отзывы могут только аутентифицированные пользователи.
*   Comment - модель комментариев. Комментарий привязан к определённому отзыву. Публиковать комментарии могут только аутентифицированные пользователи.
#### Установка.
1. Клонировать репозиторий:
```
git clone https://github.com/RenataGaripova/api-yamdb.git
cd api-yamdb
```
2. Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
3. Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
4. Перейти в каталог проекта api_yamdb:
```
cd api_yamdb
```
5. Применить миграции:
```
python3 manage.py migrate
```
6. Создать суперпользователя:
```
python3 manage.py createsuperuser
```
7. Запустить проект:
```
python3 manage.py runserver
```
8. Документация доступна по адресу: http://127.0.0.1:8000/redoc/

#### Импорт данных из csv:
*   Команды для импорта данных из csv хранятся в директории: api_yamdb/api/management/commands.
*   Для каждой модели описана своя команда. Для загрузки данных используйте: python3 manage.py <import_model>
*   Модели зависят друг от друга, стоит импортировать в таком порядке: users, categories, genres, titles, genres_titles, reviews, comments:
```
python3 manage.py users
python3 manage.py import_categories
python3 manage.py import_genres
python3 manage.py import_titles
python3 manage.py import_genres_titles
python3 manage.py import_reviews
python3 manage.py import_comments
```

#### Для работы с postman collection:
Перейти в каталог postman_collection:
```
cd postman_collection
```
Следовать инструкциям файла README.MD в этой директории.
