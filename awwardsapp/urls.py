from . import views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
path('', views.home, name='home'),
path("profile/", views.profile, name="profile"),
path("accounts/profile/", views.profile, name="profile"),
path("profile/update/", views.update_profile, name="update_profile"),
path("project/save/", views.save_project, name="save_project"),
path("project/<int:project_id>/", views.project_details, name="project_details"),
path("project/delete/<int:id>/", views.delete_project, name="delete_project"),
path("project/rate/<int:id>/", views.rate_project, name="rate_project"),
path("search/", views.search_project_title, name="search_project_title"),
path('login/', auth_views.LoginView.as_view, name='login'),
path('logout/', auth_views.LogoutView.as_view, name='logout'),
path('api/profiles/', views.ProfileList.as_view()),
path('api/projects/', views.ProjectList.as_view()), 
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
