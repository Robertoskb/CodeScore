# Generated by Django 4.2.1 on 2023-07-22 16:35

from django.db import migrations, models
import exams.models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0015_alter_exam_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_zip',
            field=models.FileField(upload_to='exams/answers/', validators=[exams.models.zip_validator]),
        ),
    ]
