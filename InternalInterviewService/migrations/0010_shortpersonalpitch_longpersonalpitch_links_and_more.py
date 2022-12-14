# Generated by Django 4.1.4 on 2022-12-26 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InternalInterviewService', '0009_alter_question_question_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('important_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_comments', to='InternalInterviewService.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('important_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_comments', to='InternalInterviewService.targetcompany')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_contact', to='InternalInterviewService.companycontacts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
