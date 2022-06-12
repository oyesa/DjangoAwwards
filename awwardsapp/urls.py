from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
  path('', views.home, name='home'),
  path('profile/', views.profile, name = 'profile'),
  path('create_profile/', views.create_profile, name = 'create_profile'),
  path('project/<int:id>/', views.project, name = 'project'),
  path('create_project/', views.create_project, name = 'create_project'),
  path('search_project/',views.search_project, name = 'search_project'),
  path('rate_project/<int:id>/', views.rate_project, name = 'rate_project'),
  path('api/profiles/', views.ProfileList.as_view()),
  path('api/projects/', views.ProjectList.as_view()),
]
