# Generated by Django 4.1.4 on 2023-01-04 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InternalInterviewService', '0024_alter_dossier_cover_letter_alter_dossier_questions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='resume'),
        ),
    ]
