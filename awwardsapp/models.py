from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models import IntegerField





# Create your models here.
class Profile(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic=CloudinaryField('image')
  bio=models.TextField(max_length=255, blank=True, null=True)
  contact=models.CharField(max_length=255, blank=True, null=True)

  #define methods
  def save_profile(self):
    self.save()

  def delete_profile(self):
    self.delete()

  @classmethod
  def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile

  def __str__(self):
    return self.user.username

class Project(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects",null=True)
  title = models.CharField(max_length=155, blank=True, null=True)
  description = models.TextField()
  location=models.CharField(max_length=50, default="Kenya")
  url=models.URLField()
  screenshot=CloudinaryField('image')
  post_date=models.DateTimeField(auto_now_add=True, null=True)

  #define methods
  def save_project(self):
      self.save()

  def update_project(self, **kwargs):
      for key, value in kwargs.items():
          setattr(self, key, value)
      self.save()

  def delete_project(self):
      self.delete()

  def __str__(self):
      return self.title

  #classmethods
  @classmethod
  def get_all_projects(cls):
      projects = cls.objects.all()
      return projects

  @classmethod
  def search_project_title(cls, search_term):
    projects= cls.objects.filter(title=search_term)
    return projects

  @classmethod
  def get_projects_by_user(cls, user):
      projects = cls.objects.filter(user=user)
      return projects
  
  @classmethod
  def get_project_by_id(cls, id):
      project = cls.objects.get(id=id)
      return project


class Vote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='votes')
  post_date=models.DateTimeField(auto_now_add=True)
  design_rate = models.IntegerField(default=0, blank=True, null=True)
  usability_rate = models.IntegerField(default=0, blank=True, null=True)
  content_rate = models.IntegerField(default=0, blank=True, null=True)
  average_rate = models.IntegerField(default=0, blank=True, null=True)

  #methods
  def save_vote(self):
    self.save()

  def delete_vote(self):
    self.delete()

  @classmethod
  def filter_by_id(cls, id):
      rating = Vote.objects.filter(id=id).first()
      return rating

  def __str__(self):
      return self.user.username


  