# Generated by Django 4.2.1 on 2023-07-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_result_need_resubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='need_resubmission',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
