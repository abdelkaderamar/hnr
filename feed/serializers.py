from .models import Story

from rest_framework import serializers

class StorySerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = 'api_url'
    class Meta:
        model = Story
        fields = [
            'api_url', 'author', 'score', 'time', 'url', 'descendants', 
            'is_top', 'is_new', 'is_best', 'is_ask', 'is_show',  'is_job'
         ] 
