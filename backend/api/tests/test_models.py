from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_emailaddress(self):
        """
        Tests if a user gets created with emailaddress
        """
        email = "test@test.com"
        password = "HelloTestThis"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_super_user(self):
        email = 'test@test.com'
        password = 'hello'
        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(superuser.is_superuser)

    def test_user_email_normalized(self):
        """
        Tests if the email of a user is normalized
        """
        email = 'TEST@test.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='hello')

        self.assertEqual(user.email, email.lower())

    def test_user_no_email(self):
        """
        Test if user gets created without emailaddress
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='hello'
            )
        