from . import views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
path('', views.home, name='home'),
re_path(r'^profile/(?P<profile_id>\d+)',views.profile,name = 'profile'),
re_path(r'^create_profile/$',views.create_profile,name = 'create_profile'),
re_path(r'^project/(?P<project_id>\d+)',views.project,name = 'project'),
re_path(r'^create_project/$',views.create_project,name = 'create_project'),
re_path(r'^search_project/$',views.search_project,name = 'search_project'),
re_path(r'^rate_project/(?P<project_id>\d+)',views.rate_project,name = 'rate_project'),
path('login/', auth_views.LoginView.as_view, name='login'),
path('logout/', auth_views.LogoutView.as_view, name='logout'),
#
path('api/profiles/', views.ProfileList.as_view()),
path('api/projects/', views.ProjectList.as_view()), 
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
