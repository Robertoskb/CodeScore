# Generated by Django 4.2.1 on 2023-05-09 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
