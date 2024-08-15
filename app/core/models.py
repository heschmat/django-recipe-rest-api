"""Database Models."""

from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,   # functionality for auth
    PermissionsMixin
)


# Create your models here.
class UserManager(BaseUserManager):
    """Manage Users."""

    def create_user(self, email, password, **kwargs):
        """Saves and returns the newly created user."""
        if not email:
            raise ValueError('Email is mandatory.')
        # `.normalize_email()` is provided by the BaseUserManager.
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)   # Saves the hashed pass.
        # `self._db` ensures it's saved to multiple databases if it's the case.
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User class."""
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    # Only staff has permission to login to admin.
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
