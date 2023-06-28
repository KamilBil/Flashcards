from django.db import models
from django.contrib.auth.models import User


class Pack(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Flashcard(models.Model):
    # TODO: img support, auto translation
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    # change to move to ungrouped
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
