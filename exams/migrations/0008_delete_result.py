# Generated by Django 4.2.1 on 2023-07-10 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0007_alter_result_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Result',
        ),
    ]