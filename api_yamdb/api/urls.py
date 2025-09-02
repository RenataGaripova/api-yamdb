from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

v1_router = SimpleRouter()
v1_router.register('categories', views.CategoryViewSet, basename='categories')
v1_router.register('genres', views.GenreViewSet, basename='genres')
v1_router.register('titles', views.TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
