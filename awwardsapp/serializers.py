from .models import Profile, Project
from rest_framework import serializers



#Serialize models here
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model=Profile
    fields=('user', 'profile_pic', 'bio', 'contact')

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model=Project
    fields = ('user', 'description', 'title', 'screenshot', 'url', 'location', 'post_date')
