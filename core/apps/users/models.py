
import uuid
import time
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **kwargs):
        if not username:
            username = uuid.uuid4().hex[:10]
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **kwargs)


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Phone Number',
        blank=True,
        null=True,
        db_index=True
    )

    objects = CustomUserManager()

    def __str__(self, *args, **kwargs):
        if self.phone_number:
            return self.phone_number
        return self.username

    def phone_no(self, *args, **kwargs):
        if self.phone_number:
            return self.phone_number
        return self.username
