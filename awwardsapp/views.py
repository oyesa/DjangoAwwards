from turtle import title
from django.http import Http404
from django.shortcuts import render, redirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, Vote
from django.contrib.auth.models import User
from django.core import exceptions









# Create your views here.
# @login_required(login_url='/accounts/login')
def home(request):
  title='Crowne Awards'
  date=dt.date.today()
  projects=Project.display_projects()
  projects_scores=projects.order_by('-average_score')
  highest_score=None
  highest_votes=None

  if len(projects)>=1:
    highest_score=projects_scores[0]
    votes=Vote.get_project_votes(highest_score.id)
    highest_votes=votes[:3]
  return render(request, 'home.html', {'title':title, 'date':date, 'votes': highest_votes, 'projects': projects, 'highest': highest_score})
 

@login_required(login_url='/accounts/login')
def profile(request, profile_id):
  try:
    user=User.objects.get(pk=profile_id)
    profile=Profile.objects.get(user=user)
    title=profile.user.username
    projects=Project.get_user_project(profile.id)
    projects_count=projects.count()
    votes=[]

    for project in projects:
      votes.append(project.average_score)
    total_votes=sum(votes)
    average=0
    if len(projects)>1:
      average=total_votes/len(projects)
  except Profile.Exception:
    raise Http404()
  return(request, 'user/profile.html', {'profile': profile, 'projects': projects, 'count':projects_count, 'average': average, 'votes': total_votes})