"""Database Models."""

from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser, # functionality for auth
    PermissionsMixin
)

# Create your models here.
class UserManager(BaseUserManager):
    """Manage Users."""

    def create_user(self, email, password, **kwargs):
        """Saves and returns the newly created user."""
        user = self.model(email= email, **kwargs)
        user.set_password(password) # Saves the hashed pass.
        # `self._db` ensures it's saved to multiple databases if it's the case.
        user.save(using= self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User class."""
    email = models.EmailField(max_length= 50, unique= True)
    name = models.CharField(max_length= 50)
    is_active = models.BooleanField(default= True)
    # Only staff has permission to login to admin.
    is_staff = models.BooleanField(default= False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
