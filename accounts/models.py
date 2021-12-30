import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.aggregates import Max
from exercises.models import Exercise 


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


class User(AbstractBaseUser, PermissionsMixin):
    """the default user model, containing essential information"""
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_active_workout(self):
        """find out if the user currently has an active Workout instance"""
        set = self.workouts.all()
        active_wo = set.filter(is_active=True).count()
        return active_wo

    def readiness_history(self):
        """Get a list of user's workout readiness ratings"""
        u = self.objects.prefetch_related('workout').prefetch_related('workout_readiness')


class Gender(models.Model):
    """genders to choose from in UserProfile"""
    name = models.CharField(max_length=40)


class TrainingPhase(models.Model):
    """
    Training phases to choose from in UserProfile
    eg. Hypertrophy, Strength, PPL
    """
    name = models.CharField(max_length=40)
    

class UserProfile(models.Model):
    """"Profile information for the User to input after signup"""
    user          = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    height        = models.PositiveSmallIntegerField(null=True)
    weight        = models.PositiveSmallIntegerField(null=True)
    birth_date    = models.DateField(null=True)
    gender        = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    training_focus= models.ForeignKey(TrainingPhase, null=True,  on_delete=models.SET_NULL)
    training_days = models.PositiveIntegerField(default=4, validators=[MinValueValidator(2), MaxValueValidator(7)])


class UserRMManager(models.Manager):
    """We want the user's highest rep max in the last 90 days"""
    def latest_one_rm(self, user, exercise):
        timeout = datetime.date.today() - datetime.timedelta(days=90)
        return super().get_queryset().filter(user=user, exercise=exercise, date__gte=timeout).aggregate(Max('one_rep_max'))


class UserRM(models.Model):
    """
    All of the User's One-Rep-Maxes for specific Exercises.
    Set by the User until they expire or are beaten.
    """
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    one_rep_max = models.PositiveIntegerField()
    date        = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.exercise} - {self.date}'

    objects = models.Manager()
    one_rm_manager = UserRMManager()


class UserMetrics(models.Model):
    """
    Calculated values based on the User's UserProfile baseline.
    Will be updated based on Workout performance in the next phase
    """
    pass
    # user      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # exercise  = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)
    # phase     = models.ForeignKey(TrainingPhase, on_delete=models.SET_NULL, null=True)
    # mev       = models.PositiveIntegerField()
    # mrv       = models.PositiveIntegerField()
    # frequency = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    #periodization