from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = "Удаляет все новости и статьи из базы данных"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f"Вы действительно хотите удалить весь контент в категории {options['category']}!? Y/N: ")

        if answer != "Y":
            self.stdout.write(self.style.ERROR("Отменено!"))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(postCategory=category).delete()
            self.stdout.write(self.style.ERROR(f"Все статьи удалены из категории{сategory.name}"))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Категория {options['category']} не найдена!"))
