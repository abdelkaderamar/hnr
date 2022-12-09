from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    keywords = models.CharField(null=True, max_length=1024)
    max_story = models.IntegerField(default=-1)
    save_and_hide = models.BooleanField(default=False)
    # Possible values for default_display
    # -2 : show +24h old stories
    # -1 : show -24h old stories
    # default : show all stories
    default_display = models.IntegerField(default=0)
    # if True open HN page by default 
    open_hn_by_default = models.BooleanField(default=False)
    open_in_new_tab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} | keywords = [{self.keywords}] | save_and_hide = [{self.save_and_hide}] | default_display = [{self.default_display}] "

    def __repr__(self):
        return self.__str__()

    OLD_STORIES = -2
    RECENT_STORIES = -1