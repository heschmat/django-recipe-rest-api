"""
Tests for the Django Admin modifications.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):

    # `unittest` module uses `setUp`; it'll be automatically called
    # before each test method, to **setUp** any state that's needed.
    # also, there is `tearDown`
    def setUp(self) -> None:
        """Create user & client."""
        # Django test client, allows to make HTTP requests.
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='this-is-admin'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            password='user1',
            name='not-admin'
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        # Get the URL for the page that shows the list of users.
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)   # admin will login; as we forced login above.
        print('=====================> ', res)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # for example this: admin/core/user/1/change/
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
