from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestClass(TestCase):
    def setUp(self):
        self.oyesa = User(username = "oyesa", email = "mercyoyesa2018@gmail.com", password = "katas")
        self.profile = Profile(user= self.oyesa, profile_pic='prof.png',bio='bio', location='Kilgoris, Kenya', email='mercyoyesa2018@gmail.com', link='www.mywebsite.com')
        self.oyesa.save()
        self.profile.save_profile()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.oyesa, User))
        self.assertTrue(isinstance(self.profile, Profile))

    def test_edit_bio(self):
        self.profile.edit_bio('To be or not to be')
        self.assertEqual(self.profile.bio, 'To be or not to be')
