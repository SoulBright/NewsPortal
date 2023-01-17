from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Post


class MyModelAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comments)
admin.site.register(UserCategory)

