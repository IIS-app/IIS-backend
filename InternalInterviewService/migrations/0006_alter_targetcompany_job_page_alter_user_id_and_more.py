# Generated by Django 4.1.4 on 2022-12-15 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InternalInterviewService', '0005_win_user_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetcompany',
            name='job_page',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='win',
            name='occured_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='win',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('IQ', 'Interview Questions'), ('CQ', 'Company Questions')], default='IQ', max_length=2)),
                ('question', models.CharField(max_length=50)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('answer', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
