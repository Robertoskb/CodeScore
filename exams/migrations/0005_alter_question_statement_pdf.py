# Generated by Django 4.2.1 on 2023-05-13 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_alter_question_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='statement_pdf',
            field=models.FileField(upload_to='exams/statements/'),
        ),
    ]
