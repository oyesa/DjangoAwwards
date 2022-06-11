from django.http import Http404
from django.shortcuts import render, redirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, Vote
from django.contrib.auth.models import User
from django.core import exceptions
from .forms import *
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *









# Create your views here.
#Homepage
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
 
#user profile
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

def create_profile(request):
    current_user = request.user
    title = "Create Profile"
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = UserProfileForm()
    return render(request, 'user/create_profile.html', {"form": form, "title": title})

#voting and average calculation 
@login_required(login_url='/accounts/login')
def project(request, project_id):
  form=VoteProjectForm()
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
    except Profile.DoesNotExist:
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

#logged in user create a project
@login_required(login_url='/accounts/login/')
def create_project(request):
    title = "Create a project"
    if request.method == "POST":
        form = AddProjectForm(request.POST, request.FILES)
        current_user = request.user
        try:
            profile = Profile.objects.get(user = current_user)
        except Profile.DoesNotExist:
            raise Http404()
        if form.is_valid():
            project = form.save(commit= False)
            project.profile = profile
            project.save()
        return redirect("home")
    else:
        form = AddProjectForm()
    return render(request, 'project/add_project.html', {"form": form, "title":title})

#search for a single project
@login_required(login_url='/accounts/login/')
def search_project(request):
    if "project" in request.GET and request.GET["project"]:
        searched_project = request.GET.get("project")
        title = "CrowneAwards | search"
        voted = False
        try:
            projects = Project.search_project(searched_project)
            count = projects.count()
            message =f"{searched_project}"
            if len(projects) == 1:
                project = projects[0]
                form = VoteProjectForm()
                title = project.name.upper()
                votes = Vote.get_project_votes(project.id)
                voters = project.voters
                
                for vote in votes:
                    try:
                        user = User.objects.get(pk = request.user.id)
                        profile = Profile.objects.get(user = user)
                        voter = Vote.get_project_voters(profile)
                        voters_list=[]
                        voted = False
                        if request.user.id in voters_list: 
                            voted = True
                    except Profile.DoesNotExist:
                        voted = False
                return render(request, 'project/project.html', {"form": form, "project": project, "voted": voted, "votes": votes, "title": title})
            return render(request, 'project/search.html', {"projects": projects,"message": message, "count":count, "title": title})
        except Project.DoesNotExist:
            suggestions = Project.display_all_projects()
            message= f"No projects titled {searched_project}"
            return render(request, 'project/search.html', {"suggestions":suggestions,"message": message, "title": title})
    else:
        message = "No term searched"
        return render(request,'project/search.html', {"message": message, "title": title})

#rating projects
@login_required(login_url='/accounts/login/')
def rate_project(request,project_id):
    if request.method == "POST":
        form = VoteProjectForm(request.POST)
        project = Project.objects.get(pk = project_id)
        current_user = request.user
        try:
            user = User.objects.get(pk = current_user.id)
            profile = Profile.objects.get(user = user)
        except Profile.DoesNotExist:
            raise Http404()

        if form.is_valid():
            vote = form.save(commit= False)
            vote.voter = profile
            vote.project = project
            vote.save_vote()
            return HttpResponseRedirect(reverse('project', args =[int(project.id)]))
    else:
        form = VoteProjectForm()
    return render(request, 'project/project.html', {"form": form})




#API Views
class ProfileList(APIView):
    def get(self,request,format = None):
        profiles =  Profile.objects.all()
        serializers = ProfileSerializer(profiles, many=True)
        return Response(serializers.data) 


class ProjectList(APIView):
    def get(self,request,format = None):
        projects =  Project.objects.all()
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data) 
