from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from guardian.shortcuts import assign_perm
from .models import Accommodation
from .forms import PropertyOwnerSignupForm



class ViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password')
        
        # Create a Property Owners group (assuming this exists in your app)
        self.group = Group.objects.create(name='Property Owners')


    def test_index(self):
        """Test that the index view returns the correct response"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Successfully Signed Up!")
