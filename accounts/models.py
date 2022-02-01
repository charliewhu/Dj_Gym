from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator

from exercises.models import Exercise, ProgressionType
from .managers import MyUserManager



class User(PermissionsMixin, AbstractBaseUser):
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

    def mean_readiness(self):
        """User's mean readiness rating over last 40 instances"""
        r = self.readiness_set.order_by('-id')[:40]
        user = User.objects.filter(id=self.pk).prefetch_related("readiness_set")
        return user


class Gender(models.Model):
    """genders to choose from in UserProfile"""
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name


class TrainingFocus(models.Model):
    """Bodybuilding, Powerbuilding, PL Hypertrophy,PL Strength, Peaking, Bridge"""
    name     = models.CharField(max_length=40)
    #what % Bodybuilding to Powerlifting etc for each of these phases?

    def __str__(self):
        return self.name


class Frequency(models.Model):
    """Upper/Lower, FullBody, PPL etc"""
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Periodization(models.Model):
    """
    Linear - weekly overload of volume/intensity
    Alternating - weekly alternation of S/B/D or U/L
    Undulating - undulating of low/medium/high sessions
    """
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    """"Profile information for the User to input after signup"""
    user          = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    height        = models.PositiveSmallIntegerField(null=True)
    weight        = models.PositiveSmallIntegerField(null=True)
    birth_date    = models.DateField(null=True)
    gender        = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    training_focus= models.ForeignKey(TrainingFocus, null=True,  on_delete=models.SET_NULL)
    training_days = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(7)])

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        """
        Check if training_focus has changed
        Check first time saved / if User already has an exercise list
        """

        exercises = Exercise.objects.filter(user=self.user)  or Exercise.objects.filter(user=None)
        try:
            current_tf = UserProfile.objects.get(pk=self.pk).training_focus
        except:
            current_tf = None

        print(exercises)
        print(current_tf)

        if self.training_focus != current_tf: #user is creating first user profile
            print("Do something - I changed my training_focus")


            for exercise in exercises:
                progression_type = ProgressionType.objects.get(
                    training_focus=self.training_focus,
                    mechanic=exercise.mechanic,
                    force=exercise.force,
                    tier=exercise.tier,
                )

                if not exercise.user: #exercise.id remains if user has exercise list
                    exercise.id = None
                exercise.user = self.user
                exercise.progression_type = progression_type
                exercise.save()

        super().save(*args,**kwargs)
