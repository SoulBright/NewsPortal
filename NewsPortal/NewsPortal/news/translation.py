from .models import Post, Category
from modeltranslation.translator import register, \
    TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода


@register(Post)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('title', 'text')  # указываем, какие именно поля надо переводить в виде кортежа


@register(Category)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
