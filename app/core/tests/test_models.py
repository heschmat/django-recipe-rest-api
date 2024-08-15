"""Test for Models."""

from django.test import TestCase

from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_success(self):
        """Test if creating a user with email is successful."""
        email = 'mai@example.com'
        password = 'changeme'
        user = get_user_model().objects.create_user(email= email, password= password)

        self.assertEqual(user.email, email)
        # We check if the hash matches for password.
        self.assertTrue(user.check_password(password))
