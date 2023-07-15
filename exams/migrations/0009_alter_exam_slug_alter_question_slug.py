# Generated by Django 4.2.1 on 2023-07-15 01:46

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0008_delete_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
    ]
