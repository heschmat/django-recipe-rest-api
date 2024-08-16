"""
Tests for the user API.
/user/
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create') # /api/usercreate/

PAYLOAD = {
            'email': 'user1@example.com',
            'password': '1234xoxo',
            'name': 'test-user',
        }


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserAPITests(TestCase):
    """unauthorized users"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        # Pass the payload to the url:
        res = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve the user from the DB with the given email;
        # to validate that the object is actually created & saved to the db.
        user = get_user_model().objects.get(email=PAYLOAD['email'])
        self.assertTrue(user.check_password(PAYLOAD['password']))
        # Make sure the `password` itself won't be saved.
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """If user already registered; return error."""
        _ = create_user(**PAYLOAD)
        # Try to create user with the same specs (specifically, with email)
        res = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Password should be at least 8 characters."""
        # Modify the payload so that it has short password:
        # This will be guaranteed via `extra_kwargs` in the `UserSerializer`.
        res = self.client.post(CREATE_USER_URL, {**PAYLOAD, 'password': '1234567'})
        # In case password is short, we sould get `BAD_REQUEST` response.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Make sure the user is not created:
        user = get_user_model().objects.filter(email=PAYLOAD['email'])
        self.assertFalse(user.exists())
