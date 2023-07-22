# Generated by Django 4.2.1 on 2023-07-22 20:28

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0018_alter_question_max_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='statement_pdf',
            field=models.FileField(upload_to='exams/statements/', validators=[utils.validators.pdf_validator]),
        ),
    ]
