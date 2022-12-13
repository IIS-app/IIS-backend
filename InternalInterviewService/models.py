from django.db import models

# Create your models here.

class Questions(models.Model):
    question=models.TextField(max_length=1000)