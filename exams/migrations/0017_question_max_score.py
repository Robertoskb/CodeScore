# Generated by Django 4.2.1 on 2023-07-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0016_alter_question_answer_zip'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='max_score',
            field=models.IntegerField(default=None, editable=False, null=True),
        ),
    ]
