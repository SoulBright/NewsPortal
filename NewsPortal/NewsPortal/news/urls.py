from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view()),  # список новостей
    path('<int:pk>/', NewsDetails.as_view(), name='news_detail'),  # Вывод конкретной статьи
    path('categories/', CategoriesList.as_view()),  # список категорий
    path("search", post_filter),  # поиск / фильтр
    path('add/', PostCreate.as_view(), name='news_create'),  # создание статьи
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),  # Редактирование статьи
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),  # Удаление статьи
    path('categories/<int:pk>/', CategoriesDetail.as_view(), name='categories_detail')    # Список статей в категории
]
