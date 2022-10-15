from email.policy import default
from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=1024, null=False)
    author=models.CharField(max_length=128, null=False)
    score=models.IntegerField()
    time=models.DateTimeField()
    url=models.CharField(max_length=1024, null=False)
    descendants=models.IntegerField(default=0)
    is_top = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_best = models.BooleanField(default=False)
    is_ask = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    is_job = models.BooleanField(default=False)
    
class UserStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    story = models.ForeignKey(Story, on_delete=models.PROTECT)
    saved = models.BooleanField(default=False)
    ignored = models.BooleanField(default=False)
