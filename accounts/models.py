from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from feeds.models import Article

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email='balgabekov9@gmail.com', password=None):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    Inhertiance from the AbstractBaseUser is used
    to avoid changing the default user model.

    Main difference from the default model:
        - bookmarks
    """
    username = models.CharField(max_length=45, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=45)
    second_name = models.CharField(max_length=45)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    bookmarks = models.ManyToManyField(Article)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

