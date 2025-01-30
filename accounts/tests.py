from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile

CustomUser = get_user_model()

class CustomUserModelTests(TestCase):

    def setUp(self):
        # Creating a test user
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="strongpassword123",
            first_name="Test",
            last_name="User",
            birthdate="2000-01-01"
        )

    def test_user_creation(self):
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)  # Ensure one user has been created.
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("strongpassword123"))

    def test_user_profile_created(self):
        # A user profile should be automatically created upon user creation
        self.assertIsNotNone(self.user.userprofile)
        self.assertEqual(self.user.userprofile.last_calories, 0.0)

    def test_super_user_creation(self):
        super_user = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User"
        )
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "test@example.com")
        
class UserProfileModelTests(TestCase):
    
    def setUp(self):
        # Creating a test user also creates a UserProfile due to signal
        self.user = CustomUser.objects.create_user(
            email="profile_test@example.com",
            password="strongpassword123",
            first_name="Profile",
            last_name="User",
            birthdate="2000-01-01"
        )
    
    def test_userprofile_defaults(self):
        profile = self.user.userprofile
        self.assertEqual(profile.last_calories, 0.0)
        self.assertEqual(profile.last_protein, 0.0)
        self.assertEqual(profile.last_carbs, 0.0)
        self.assertEqual(profile.last_fats, 0.0)

    def test_user_profile_string_representation(self):
        profile = self.user.userprofile
        self.assertEqual(str(profile), "profile_test@example.com Profile")

    def test_update_user_profile(self):
        profile = self.user.userprofile
        profile.last_calories = 2500.0
        profile.save()
        self.assertEqual(profile.last_calories, 2500.0)

class UserAPITests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        # Create a test user and obtain a token for them
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="strongpassword123",
            first_name="Test",
            last_name="User"
        )
        self.user_profile = UserProfile.objects.get(user=self.user)

        # Log in to get a valid token
        response = self.client.post(reverse('login'), {'username': 'test@example.com', 'password': 'strongpassword123'})
        self.token = response.data['token'] if 'token' in response.data else None
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'birthdate': '1990-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())

    def test_user_login(self):
        url = reverse('login')
        data = {
            'username': 'test@example.com',
            'password': 'strongpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_view_user_profile(self):
        url = reverse('userprofile-detail', kwargs={'pk': self.user_profile.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Validate the fields that are part of the response
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['birthdate'], str(self.user.birthdate))  # Ensure correct formatting

    def test_update_user_profile(self):
        url = reverse('userprofile-detail', kwargs={'pk': self.user_profile.pk})
        data = {'last_calories': 2200.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.last_calories, 2200.0)

    def test_user_logout(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        url = reverse('userprofile-detail', kwargs={'pk': self.user_profile.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserProfile.objects.filter(pk=self.user_profile.pk).exists())

    def test_change_user_password(self):
        # Test that a user can successfully change their password
        url = reverse('change_password')
        data = {
            'old_password': 'strongpassword123',
            'new_password': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the new password works by logging in again
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_change_password_with_wrong_old_password(self):
        # Validate error response when providing wrong old password
        url = reverse('change_password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_non_matching_confirm(self):
        # Ensure non-matching new passwords fail as expected
        url = reverse('change_password')
        data = {
            'old_password': 'strongpassword123',
            'new_password': 'newpassword123',
            'new_password2': 'differentpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)