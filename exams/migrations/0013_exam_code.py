# Generated by Django 4.2.1 on 2023-07-15 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0012_rename_avaliable_exam_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='code',
            field=models.CharField(default='a', max_length=6),
            preserve_default=False,
        ),
    ]
