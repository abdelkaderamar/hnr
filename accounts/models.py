from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    keywords = models.CharField(null=True, max_length=1024)
    max_story = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.user} | keywords = [{self.keywords}]"

    def __repr__(self):
        return self.__str__()