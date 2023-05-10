# Generated by Django 4.2.1 on 2023-05-09 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_exam_slug_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
