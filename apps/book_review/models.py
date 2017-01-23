from __future__ import unicode_literals
from django.contrib.auth.models import UserManager
from django.db import models

class users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()
    def __str__(self):
        return self.password

class books(models.Model):
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    objects = UserManager()

class reviews(models.Model):
    review = models.CharField(max_length = 1000)
    user = models.ForeignKey('users')
    book = models.ForeignKey('books')
    objects = UserManager()
