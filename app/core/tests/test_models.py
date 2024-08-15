"""Test for Models."""

from django.test import TestCase

from django.contrib.auth import get_user_model


def normalize_email(email):
    """Normalize the email by lowercasing the domain part."""
    local, domain = email.split('@')
    return f'{local}@{domain.lower()}'


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_success(self):
        """Test if creating a user with email is successful."""
        email = 'mai@example.com'
        password = 'changeme'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        # We check if the hash matches for password.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Make sure emails for new users are normalized."""
        sample_emails = [
            'test1@EXAMPLE.com',
            'Test2@Example.com',
            'TEST3@EXAMPLE.COM',
            'test4@example.COM',
        ]

        for email in sample_emails:
            user = get_user_model().objects.create_user(email, password='1234')
            self.assertEqual(user.email, normalize_email(email))

    def test_new_user_without_email_raises_error(self):
        """Creating a user w/o an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='1234')

    def test_create_superuser(self):
        # .create_superuser() will be defined in `models.py` in `UserManager` class.
        user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='this_is_superuser!!!'
        )
        # `is_superuser` & `is_staff` are provided by PermissionsMixin:
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
