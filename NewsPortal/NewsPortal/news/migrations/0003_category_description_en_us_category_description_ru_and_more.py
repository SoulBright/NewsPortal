# Generated by Django 4.0.4 on 2022-12-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_usercategory_category_subscribers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_en_us',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ru',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
