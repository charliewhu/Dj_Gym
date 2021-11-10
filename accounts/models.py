from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator

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
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_pic = models.ImageField(
        default="profile1.png", null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_active_workout(self):
        set = self.workouts.all()
        active_wo = set.aggregate(sum=models.Sum('is_active'))['sum']
        return active_wo

    def readiness_history(self):
        u = self.objects.select_related('workout'). prefetch_related('workout_readiness')


class Gender(models.Model):
    name = models.CharField(max_length=40)


class TrainingPhase(models.Model):
    name = models.CharField(max_length=40)
    

class UserProfile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    height        = models.PositiveSmallIntegerField(null=True)
    weight        = models.PositiveSmallIntegerField(null=True)
    birth_date    = models.DateField(null=True)
    gender        = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    training_focus= models.ForeignKey(TrainingPhase, null=True,  on_delete=models.SET_NULL)
    training_days = models.PositiveIntegerField(default=4, validators=[MinValueValidator(2), MaxValueValidator(7)])


class UserRM(models.Model):
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exercise    = models.ForeignKey(Exercise)
    one_rep_max = models.PositiveIntegerField()
    date        = models.DateField(auto_now=True)


class UserMetrics(models.Model):
    user      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exercise  = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)
    phase     = models.ForeignKey(TrainingPhase, on_delete=models.SET_NULL, null=True)
    mev       = models.PositiveIntegerField()
    mrv       = models.PositiveIntegerField()
    frequency = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    #periodization