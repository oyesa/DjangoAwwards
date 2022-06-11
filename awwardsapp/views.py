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



@login_required(login_url='/accounts/login')
def project(request, project_id):
  # form=RateProjectForm()
  project = Project.objects.get(pk=project_id)
  title=project.name.title()
  votes=Vote.get_project_votes(project.id)
  total_votes=votes.count()
  voted=False

  voters_list=[]
  average_list=[]
  design_list=[]
  usability_list=[]
  content_list=[]
  for vote in votes:
    voters_list.append(vote.voter.id)
    average_sum=vote.design + vote.usability + vote.content
    average=average_sum/3
    average_list.append(average)
    design_list.append(vote.design)
    usability_list.append(vote.usability)
    content_list.append(vote.content)

    try:
      user=User.objects.get(pk=request.user.id)
      profile=Profile.objects.get(user=user)
      voter=Vote.get_voters(profile)
      voted=False
      if request.user.id in voters_list:
        voted=True
    except Profile.Exception:
      voted=False
  print('USER')
  print(request.user.id)
  print(project.profile.user.id)
  average_score=0
  average_design=0
  average_usability=0
  average_content=0
  if len(average_list)>0:
    average_score=sum(average_list) / len(average_list)
    project.average_score=average_score
    project.save()
  if total_votes !=0:
    average_design = sum(design_list) / total_votes
    average_usability = sum(usability_list) / total_votes 
    average_content = sum(content_list) / total_votes
    project.average_design = average_design
    project.average_usability = average_usability
    project.average_content =average_content
    project.save()

  return render(request, 'project/project.html', {"title": title, "form": form, "project": project, "votes": votes, "voted": voted, "total_votes":total_votes})










    
