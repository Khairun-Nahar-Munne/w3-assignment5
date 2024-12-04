from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import assign_perm

from .models import Accommodation
from .forms import PropertyOwnerSignupForm


class ViewTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )

        # Create Property Owners group
        self.property_owners_group, _ = Group.objects.get_or_create(name='Property Owners')


    def test_property_owner_signup_get(self):
        """
        Test accessing the signup page
        """
        url = reverse('property_owner_signup')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], PropertyOwnerSignupForm)

    

    def test_property_owner_signup_post_invalid(self):
        """
        Test property owner signup with invalid data
        """
        # Prepare invalid signup data (passwords don't match)
        signup_data = {
            'username': 'newowner',
            'email': 'newowner@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'DifferentPassword456!'
        }

        url = reverse('property_owner_signup')
        response = self.client.post(url, signup_data)

        # Should render signup page again with form errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_index_view(self):
        """
        Test the index view
        """
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Home Page")