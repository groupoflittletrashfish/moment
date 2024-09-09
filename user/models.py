from django.db import models


class Info(models.Model):
    ip = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    full_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    created_date = models.DateTimeField()
    created_by = models.CharField(max_length=32)
    updated_date = models.DateTimeField
    updated_by = models.CharField(max_length=32)
