from tkinter.constants import CASCADE

from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Purchased_Items (models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=CASCADE)
    def __str__(self):
        return self.name
