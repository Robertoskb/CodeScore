# Generated by Django 4.2.1 on 2023-07-17 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_alter_result_solution_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]