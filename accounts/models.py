from xml.dom import HierarchyRequestErr
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator

from exercises.models import Exercise, Force, ProgressionType, ProgressionTypeAllocation
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
        TrainingFocus, null=True,  on_delete=models.SET_NULL)
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
        # self.reassign_exercises()
        super().save(*args, **kwargs)
        # self.assign_split()

    def should_have_split(self):
        return not self.split and self.training_focus and self.training_days

    def get_split_from_frequency_allocation(self):
        return FrequencyAllocation.objects.get(
            training_focus=self.training_focus,
            training_days=self.training_days,
            hierarchy=1,
        ).split

    def assign_split(self):
        if self.should_have_split():
            self.split = self.get_split_from_frequency_allocation()
            self.save()

    def split_days_count(self):
        """returns the number of days in the split"""
        return self.split.splititem_set.count()

    def is_training_focus_changed(self):
        """
        Returns True if the user's training focus has changed.
        Must be called pre-save()
        """
        prev_training_focus = User.objects.filter(
            id=getattr(self.id, None)).first().training_focus
        return prev_training_focus != self.training_focus

    def reassign_exercises(self):
        """
        assign all of the default (user=null) exercises to this user
        """
        exercises = Exercise.objects.filter(
            user=self) or Exercise.objects.filter(user=None)
        for exercise in exercises:
            # find progression_type based on UserProfile & Exercise attributes
            # logically equivalent to a JOIN on all of these fields
            progression_type_allocation = ProgressionTypeAllocation.objects.get(
                training_focus=self.training_focus,
                mechanic=exercise.mechanic,
                tier=exercise.tier,
            )

            if not exercise.user:  # exercise.id remains if user has exercise list
                exercise.id = None
            exercise.user = self
            exercise.progression_type = progression_type_allocation.progression_type
            exercise.min_reps = progression_type_allocation.min_reps
            exercise.max_reps = progression_type_allocation.max_reps
            exercise.save()

    def has_active_workout(self):
        """find out if the user currently has an active Workout instance"""
        set = self.workouts.all()
        active_wo = set.filter(is_active=True).count()
        return active_wo

    def mean_readiness(self):
        """User's mean readiness rating over last 40 instances"""
        r = self.readiness_set.order_by('-id')[:40]
        user = User.objects.filter(
            id=self.pk).prefetch_related("readiness_set")
        return user


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
        return f'{self.training_focus}, {self.split}, Days: {self.training_days}, Tier: {self.hierarchy}'

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
