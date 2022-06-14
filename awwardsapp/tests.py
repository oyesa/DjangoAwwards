from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestClass(TestCase):
    def setUp(self):
        self.oyesa = User(username = "oyesa", email = "mercyoyesa2018@gmail.com", password = "karas")
        self.profile = Profile(user= self.oyesa, profile_pic='prof-pic.png',bio='bio', location='Kilgoris, Kenya', email='mercyoyesa2018@gmail.com', url='www.mywebsite.com')
        self.oyesa.save()
        self.profile.save_profile()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.oyesa, User))
        self.assertTrue(isinstance(self.profile, Profile))



class ProjectTestClass(TestCase):
    def setUp(self):
        self.oyesa = User(username = "oyesa", email = "mercyoyesa2018@gmail.com",password = "karas")
        self.profile = Profile(user= self.oyesa, profile_pic='prof-pic.png',bio='bio', location='Kilgoris, Kenya', email='mercyoyesa2018@gmail.com', link='www.mywebsite.com')
        self.project = Project(name= "Test Project", screenshot = "screenshot.jpg", description ="project zero first test case", url = "testurl", profile= self.profile)

        self.oyesa.save()
        self.profile.save_profile()
        self.project.save_project()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Project.objects.all().delete()

    def test_image_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_project(self):
        projects = Project.objects.all()
        self.assertTrue(len(projects)> 0)

    def test_delete_project(self):
        projects1 = Project.objects.all()
        self.assertEqual(len(projects1),1)
        self.project.delete_project()
        projects2 = Project.objects.all()
        self.assertEqual(len(projects2),0)

    def test_search_project(self):
        project = Project.search_project_title('test')
        self.assertEqual(len(project),1)


# class VoteTestClass(TestCase):
#     def setUp(self):
#         self.oyesa = User(username = "oyesa", email = "mercyoyesa2018@gmail.com",password = "karas")
#         self.profile = Profile(user= self.oyesa, profile_pic='prof-pic.png',bio='bio', location='Kilgoris, Kenya', email='lmercyoyesa2018@gmail.com', link='www.mywebsite.com')
#         self.project = Project(name= "Test Project", screenshot = "screenshot.jpg", description ="project zero first test case", url = "testurl", profile= self.profile)
#         self.vote = Vote(voter=self.profile, project=self.project, design= 9, usability= 6, content = 8)

#         self.oyesa.save()
#         self.profile.save_profile()
#         self.project.save_project()
#         self.vote.save_vote()

#     def tearDown(self):
#         Profile.objects.all().delete()
#         User.objects.all().delete()
#         Project.objects.all().delete()
#         Vote.objects.all().delete()

#     def test_instance(self):
#         self.assertTrue(isinstance(self.vote, Vote))

#     def test_save_vote(self):
#         votes = Vote.objects.all()
#         self.assertTrue(len(votes)> 0)

#     def test_delete_vote(self):
#         votes1 = Vote.objects.all()
#         self.assertEqual(len(votes1),1)
#         self.vote.delete_vote()
#         votes2 = Vote.objects.all()
#         self.assertEqual(len(votes2),0)
