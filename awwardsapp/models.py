import profile
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models import IntegerField




# Create your models here.
class Profile(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic=CloudinaryField('Profile Picture')
  bio=models.TextField()
  email=models.EmailField()
  url=models.URLField()
  location=models.CharField(max_length=50)

  #define methods
  def save_profile(self):
    self.save()

  def edit_bio(self, new_bio):
    self.bio=new_bio
    self.save()

  def delete_profile(self):
    self.delete()

  def __str__(self):
    return self.user.username

class Project(models.Model):
  name=models.CharField(max_length=50)
  description=models.TextField()
  url=models.URLField()
  screenshot=CloudinaryField('Project Screenshot')
  voters=models.IntegerField(default=0)
  profile=models.ForeignKey(Profile, on_delete=models. CASCADE)
  post_date=models.DateTimeField(auto_now_add=True, null=True)
  

  #methods
  def save_project(self):
    self.save()

  def delete_project(self):
    self.delete()

  def vote_count(self):
    return self.vote.count()

  def __str__(self):
    return self.name

  #classmethods
  @classmethod
  def get_user_project(cls, profile):
    return cls.objects.filter(profile=profile)

  @classmethod
  def display_projects(cls):
    return cls.objects.all()

  @classmethod
  def search_project(cls, name):
    return cls.objects.filter(name=name)

  class Meta:
    ordering=['-post_date']


class Vote(models.Model):
  project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='votes')
  voter=models.ForeignKey(Profile, on_delete=models.CASCADE)
  post_date=models.DateTimeField(auto_now_add=True)
  #voting critirea and scale
  design = IntegerField(default=0)
  usability = IntegerField(default=0)
  content = IntegerField(default=0)

  #methods
  def save_vote(self):
    self.save()

  def delete_vote(self):
    self.delete()

  @classmethod
  def get_project_votes(cls, project):
    return cls.objects.filter(project=project)

  @classmethod
  def get_voters(cls, voter):
    return cls.objects.filter(voter=voter)

  class Meta:
    ordering=['-post_date']


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

  