from .models import Story

from rest_framework import serializers

class StorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Story
        fields = [
            'author', 'score', 'time', 'url', 'descendants', 
            'is_top', 'is_new', 'is_best', 'is_ask', 'is_show',  'is_job'
         ] 
