from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
USER_URL = reverse('users:user')

def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)

class PublicUserApiTests(TestCase):
    "Test public API for users"

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload
        """
        payload = {
            'email': 'test@test.com',
            'password': 'hello',
            'name': 'Test1 Test2',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)
    
    def test_user_exists(self):
        """
        Test creating a user that exists
        """
        payload = {
            'name': 'Test1 Test2',
            'email': 'test@test.com',
            'password': 'hello'
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_password_length(self):
        """
        Tests if password is long enough
        """
        payload = {
            'name': 'Test1 Test2',
            'email': 'test@test.com',
            'password': 'p'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_user(self):
        """
        Test that a token is created for a user
        """
        payload = {
            'email': 'test@test.com',
            'password': 'hello',
        }

        create_user(**payload)

        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid(self):
        """
        Test that a token doesnt get created if user gets invalid data
        """
        create_user(email='test@test.com', password='hello')
        payload = {
            'email': 'test@test.com',
            'password': 'goodbye',
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token doesnt get created if there is no user
        """
        payload = {
            'email': 'test@test.com',
            'password': 'hello',
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that email and password are both required
        """
        payload = {
            'email': 'test@test.com',
            'password': ''
        }
        response = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_authentication_required(self):
        """
        Test if authentication is required to update user accounts
        """
        response = self.client.get(USER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Tests private part of API
    """
    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='hello',
            name='test1 test2'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test if right profile gets returned
        """
        response = self.client.get(USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
            {
                'name': self.user.name,
                'email': self.user.email,
            })
    
    def test_post_user_not_allowed(self):
        """
        Test that post is not allowed on the user URL
        """
        response = self.client.post(USER_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """
        Test updating user
        """
        payload = {
            'name': 'Test2',
            'password': 'goodbye',
        }

        response = self.client.patch(USER_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)