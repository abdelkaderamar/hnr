from django.db import models

class Story(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=1024, null=False)
    author=models.CharField(max_length=128, null=False)
    score=models.IntegerField()
    time=models.DateTimeField()
    url=models.CharField(max_length=1024, null=False)
    descendants=models.IntegerField(default=0)
    class Meta:
        abstract = True

class TopStory(Story):
    pass

class NewStory(Story):
    pass

class BestStory(Story):
    pass

class AskStory(Story):
    pass

class ShowStory(Story):
    pass

class JobStory(Story):
    pass