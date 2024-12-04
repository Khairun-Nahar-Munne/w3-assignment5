from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import PropertyOwnerSignupForm  

class PropertyOwnerSignupFormTest(TestCase):
    def setUp(self):
        # Create a test user to check for existing username and email
        User.objects.create_user(
            username='existinguser', 
            email='existing@example.com', 
            password='testpassword123'
        )

    def test_valid_form_submission(self):
        """
        Test that a form with valid data creates a user successfully
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'strongpassword123'
        }
        form = PropertyOwnerSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        
        # Verify user was created correctly
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        
        # Verify password is set correctly (hashed)
        self.assertTrue(user.check_password('strongpassword123'))

    def test_duplicate_username(self):
        """
        Test that form fails with an existing username
        """
        form_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'strongpassword123'
        }
        form = PropertyOwnerSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(
            form.errors['username'][0], 
            "This username is already in use."
        )

    def test_duplicate_email(self):
        """
        Test that form fails with an existing email
        """
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'strongpassword123'
        }
        form = PropertyOwnerSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0], 
            "This email address is already in use."
        )

    def test_password_minimum_length(self):
        """
        Test that password must be at least 8 characters
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'short'  # Less than 8 characters
        }
        form = PropertyOwnerSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_required_fields(self):
        """
        Test that all fields are required
        """
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password']
        
        for field in required_fields:
            form_data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'strongpassword123'
            }
            # Remove the current field
            del form_data[field]
            
            form = PropertyOwnerSignupForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)

    def test_max_length_constraints(self):
        """
        Test max length constraints for fields
        """
        form_data = {
            'username': 'a' * 51,  # Exceeds max length
            'email': 'a' * 40 + '@example.com',  # Exceeds max length
            'first_name': 'a' * 51,  # Exceeds max length
            'last_name': 'a' * 51,  # Exceeds max length
            'password': 'strongpassword123'
        }
        form = PropertyOwnerSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Check that username, email, first_name, last_name exceed max length
        max_length_fields = ['username', 'email', 'first_name', 'last_name']
        for field in max_length_fields:
            self.assertIn(field, form.errors)