from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db.models import aggregates 


# define what we want to happen when a new user is created
class MyUserManager(BaseUserManager):
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
        return self.is_admin

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


class TrainingFocus(models.Model):
    name = models.CharField(max_length=40)
    

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    birth_date = models.DateField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    training_focus = models.ForeignKey(TrainingFocus, null=True,  on_delete=models.SET_NULL)







class UserGroup(models.Model):
    description = models.CharField(max_length=100)
    users       = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.description