from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='hello',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test_user@test.com',
            password='hello',
            name='Test1 Test2',
        )
    
    def test_users_listed(self):
        """
        Test that users are listed on user page
        """
        url = reverse('admin:api_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)