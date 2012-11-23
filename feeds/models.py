from django.db import models
from django.contrib.auth.models import Group, Permission, User

class Templar(models.Model):
    user = models.ForeignKey(User)
    public_key = models.CharField(max_length=250, unique=True)
    pw_encrypted = models.TextField()
    avatar = models.TextField()

class Feed(models.Model):
    owner = models.ForeignKey(Templar)
    public_key = models.CharField(max_length=250, unique=False, null=False)

class Message(models.Model):
    feed = models.ForeignKey(Feed)
    message = models.CharField(max_length=250, unique=False, null=False)

