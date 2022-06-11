from cProfile import Profile
from rest_framework import serializers

from awwardsapp.models import Project




#Serialize models here
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model=Profile
    fields=('user', 'profile_pic', 'bio', 'location', 'email', 'url')

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model=Project
    fields = ('name', 'description','screenshot', 'link', 'profile', 'post_date', 'average_design', 'average_content', 'average_score', 'average_usability')
