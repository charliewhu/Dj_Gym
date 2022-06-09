from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q

from exercises.models import Exercise, Force
from .managers import MyUserManager


class Gender(models.Model):
    """genders to choose from in UserProfile"""
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class TrainingFocus(models.Model):
    """Bodybuilding, Powerbuilding, PL Hypertrophy,PL Strength, Peaking, Bridge"""
    name = models.CharField(max_length=40)
    # what % Bodybuilding to Powerlifting etc for each of these phases?

    def __str__(self):
        return self.name


class Split(models.Model):
    """Upper/Lower, FullBody, PPL, PHUL, PHAT etc"""
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    def get_first_split_day(self):
        """returns the first SplitDay of the Split"""
        return self.splitday_set.first()


class SplitItem(models.Model):
    """eg Upper"""
    split = models.ForeignKey(Split, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class SplitDay(models.Model):
    """eg Upper Push"""
    split_item = models.ForeignKey(SplitItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    force = models.ManyToManyField(Force, through='SplitDayForce')
    order = models.PositiveIntegerField(null=True)

    # TODO -- add unique contraint on split_item + order

    def __str__(self):
        return f'{self.order}, {self.split_item}, {self.name}'


class SplitDayForce(models.Model):
    """Link table between SplitDay and Force"""
    day = models.ForeignKey(SplitDay, on_delete=models.CASCADE)
    force = models.ForeignKey(Force, on_delete=models.CASCADE)
    hierarchy = models.PositiveIntegerField()

    # TODO -- add unique contraint on day + force + hierarchy

    def __str__(self):
        return f'{self.day}, {self.force}, {self.hierarchy}'


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
    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    birth_date = models.DateField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    training_focus = models.ForeignKey(
        TrainingFocus, null=True, on_delete=models.SET_NULL)
    training_days = models.PositiveIntegerField(
        default=4, validators=[MinValueValidator(1), MaxValueValidator(7)])
    split = models.ForeignKey(
        Split, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        is_new = self.is_new()
        super().save(*args, **kwargs)
        if is_new:
            self.assign_default_exercises()
        # self.assign_split()

    def is_new(self):
        """returns true if user is new"""
        return self.pk is None

    def assign_default_exercises(self):
        exercises = Exercise.objects.all()

        for exercise in exercises:
            print("exercises: ", exercise)
            if exercise.user is None:  # exercise.id remains if user owns exercise
                exercise.id = None
            exercise.user = self
            exercise.save()

    def get_exercises(self):
        """returns all exercises for this user"""
        return Exercise.objects.filter(user=self)


class FrequencyAllocation(models.Model):
    """
    Lookup table
    When User completes profile, their choices determine their split
    """
    training_focus = models.ForeignKey(TrainingFocus, on_delete=models.CASCADE)
    training_days = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)])
    hierarchy = models.PositiveIntegerField()
    split = models.ForeignKey(Split, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.training_focus}, {self.split}, Days: {self.training_days}, Hierarchy: {self.hierarchy}'

    # TODO add unique constraints for hierarchy per training days per TrainingFocus


class Periodization(models.Model):
    """
    Linear - weekly overload of volume/intensity
    Alternating - weekly alternation of S/B/D or U/L
    Undulating - undulating of low/medium/high sessions
    """
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
