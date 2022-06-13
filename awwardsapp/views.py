from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, Vote
from django.contrib.auth.models import User
from .forms import *
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# from .permissions import IsAdminOrReadOnly
from .serializers import *

import cloudinary
import cloudinary.uploader
import cloudinary.api



# Create your views here.

def home(request):
  project=Project.objects.all()
#   latest_project=project[0]
#   rating= Vote.objects.filter(project_id=latest_project.id).first()

  return render(request, 'home.html', {"projects": project})
 
#user profile
@login_required(login_url='/accounts/login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    project = Project.objects.filter(user_id=current_user.id).all()

    return render(request, "profile.html", {"profile": profile, "screenshots": project})


@login_required(login_url="/accounts/login/")
def update_profile(request):
    if request.method == "POST":
        current_user = request.user
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        bio = request.POST["bio"]
        contact = request.POST["contact"]

        profile_image = request.FILES["profile_pic"]
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image["url"]

        user = User.objects.get(id=current_user.id)
        if Profile.objects.filter(user_id=current_user.id).exists():
            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_url
            profile.bio = bio
            profile.contact = contact
            profile.save()
        else:
            profile = Profile(
                user_id=current_user.id,
                profile_photo=profile_url,
                bio=bio,
                contact=contact,
            )
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect("/profile", {"success": "Profile update successful"})
    else:
        return render(request, "profile.html", {"danger": "Profile update unsuccessful"})

#project views 
def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    rating = Vote.objects.filter(project=project)
    return render(request, "project.html", {"project": project, "rating": rating})

@login_required(login_url="/accounts/login/")
def save_project(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST["title"]
        location = request.POST["location"]
        description = request.POST["description"]
        url = request.POST["url"]
        screenshot = request.FILES["image"]
        screenshot = cloudinary.uploader.upload(screenshot, crop="limit", width=500, height=500) # set image size
        image_url = screenshot["url"]

        project = Project(
            user_id=current_user.id,
            title=title,
            location=location,
            description=description,
            url=url,
            screenshot=image_url,
        )
        project.save_project()

        return redirect("/profile", {"success": "Project Saved Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Project Save Failed"})


#rate projects
@login_required(login_url='/accounts/login/')
def rate_project(request, id):
    if request.method == "POST":
        project = Project.objects.get(id=id)
        current_user = request.user
        design_rate=request.POST["design"]
        usability_rate=request.POST["usability"]
        content_rate=request.POST["content"]

        Vote.objects.create(
            project=project,
            user=current_user,
            design_rate=design_rate,
            usability_rate=usability_rate,
            content_rate=content_rate,
            average_rate=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),
        )
        average_rating= (int(design_rate)+int(usability_rate)+int(content_rate))/3
        project.rate=average_rating
        project.update_project()

        return render(request, "project.html", {"success": "Project Rated!", "project": project, "rating": Vote.objects.filter(project=project)})
    else:
        project = Project.objects.get(id=id)
        return render(request, "project.html", {"danger": "Rating Failed", "project": project})


# search for project
def search_project_title(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_projects = Project.objects.filter(title=search_term)
        message = f"Search For: {search_term}"

        return render(request, "search.html", {"message": message, "projects": searched_projects})
    else:
        message = "No term searched, please input search term"
        return render(request, "search.html", {"message": message})


# delete project
@login_required(login_url="/accounts/login/")
def delete_project(request, id):
    project = Project.objects.get(id=id)
    project.delete_project()
    return redirect("/profile", {"success": "Project Deleted"})


  

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
