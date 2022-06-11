from django import forms
from django.forms import ModelForm
from .models import *



#create form classes
class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class VoteProjectForm(ModelForm):
    class Meta:
        model = Vote
        exclude = ['post_date', 'voter', 'project'] 

class AddProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['profile', 'post_date', 'voters', 'design_score','usability_score','content_score','average_design','average_usability','average_content','average_score']
