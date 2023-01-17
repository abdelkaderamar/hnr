from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    OLD_STORIES = -2
    RECENT_STORIES = -1

    STORIES_PER_PAGE = 25
    HIGHLIGHT_SCORE_THRESHOLD = 50
    HIGHLIGHT_COMMENT_THRESHOLD = 50

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    keywords = models.CharField(null=True, max_length=1024)
    story_per_page = models.IntegerField(default=STORIES_PER_PAGE)
    save_and_hide = models.BooleanField(default=False)
    # Possible values for default_display
    # -2 : show +24h old stories
    # -1 : show -24h old stories
    # default : show all stories
    default_display = models.IntegerField(default=0)
    # if True open HN page by default 
    open_hn_by_default = models.BooleanField(default=False)
    open_in_new_tab = models.BooleanField(default=False)
    startup_page = models.CharField(max_length=128, null=True)
    hightlight_score_threshold = models.IntegerField(default=HIGHLIGHT_SCORE_THRESHOLD)
    hightlight_comment_threshold = models.IntegerField(default=HIGHLIGHT_COMMENT_THRESHOLD)
    def __str__(self):
        return f"{self.user} | keywords = [{self.keywords}] | save_and_hide = [{self.save_and_hide}] | default_display = [{self.default_display}] "

    def __repr__(self):
        return self.__str__()

