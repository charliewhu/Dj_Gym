import datetime
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.aggregates import Max


class MyUserManager(BaseUserManager):
    """define what we want to happen when a new user is created"""
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserRMManager(models.Manager):
    """We want the User's highest rep max, for specific Exercise, in the last 90 days"""
    def latest_one_rm(self, user, exercise):
        timeout = datetime.date.today() - datetime.timedelta(days=90)
        return \
            super()\
            .get_queryset()\
            .filter(user=user, exercise=exercise, date__gte=timeout)\
            .aggregate(Max('one_rep_max'))