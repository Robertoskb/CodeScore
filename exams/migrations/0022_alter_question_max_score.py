# Generated by Django 4.2.1 on 2023-07-22 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0021_alter_question_max_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='max_score',
            field=models.IntegerField(editable=False, null=True),
        ),
    ]
