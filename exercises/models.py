from django.conf import settings
from django.db import models
from django.apps import apps

from .managers import UserRMManager
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator


class Rir(models.Model):
    rir = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    percent = models.FloatField()


class Tier(models.Model):
    """
    T1 eg Squat, Bench
    T2 eg Paused Squat, CG Bench
    T3 eg Split Squat, DB Bench
    T4 eg Leg Extension, Pec Fly
    """
    hierarchy = models.PositiveIntegerField(null=True, unique=True)
    name = models.CharField(max_length=20, unique=True)
    # add description

    class Meta:
        ordering = ['hierarchy']

    def __str__(self):
        return self.name


class Purpose(models.Model):
    """Squat, Bench, Deadlift, Other"""
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Mechanic(models.Model):
    """Compound, Isolation"""
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Force(models.Model):
    """Hip Hinge, Vertical Push etc"""
    name = models.CharField(max_length=60, unique=True)
    base_weekly_sets = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=20, unique=True)
    force = models.ManyToManyField(Force)

    def __str__(self):
        return self.name


class ProgressionType(models.Model):
    """
    Topset Backdown eg 100x5, 80x5x5, 
    Topset-RepLower eg 100x5, 100x3x2, 
    Straight eg 100x5x5, 
    Rep-drop eg 100x9,8,7,5, 
    Technique eg 8x3 @ 5+RIR, 
    Ladder eg 100x2,9,3,8,4,6,5, 
    Pyramid eg 2,4,6,8,6,4,2
    """
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class ProgressionTypeAllocation(models.Model):
    """Allocates progression_type to exercises depending on User TrainingFocus"""
    training_focus = models.ForeignKey(
        "accounts.TrainingFocus", on_delete=models.CASCADE, null=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(
        ProgressionType, on_delete=models.CASCADE, null=True)
    min_reps = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(20)])
    max_reps = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(30)])
    min_rir = models.PositiveIntegerField(
        null=True, default=1, validators=[MaxValueValidator(5)])
    max_rir = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(5)])

    def __str__(self):
        return f'{self.training_focus}, {self.mechanic}, {self.tier}, {self.progression_type}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['training_focus', 'mechanic', 'tier'], name="UniqueProgressionTypeCheck")
        ]


class Exercise(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    force = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(
        ProgressionType, on_delete=models.CASCADE, null=True, blank=True)
    min_reps = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(20)])
    max_reps = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(30)])
    min_rir = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(5)])
    max_rir = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(5)])
    is_active = models.BooleanField(default=1)
    is_unilateral = models.BooleanField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="UserUniqueExercise")
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.is_new()
        self.set_progression_type()
        super().save(*args, **kwargs)
        if is_new and not self.has_user():
            self.set_exercise_to_users()

    def set_progression_type(self):
        try:
            prog_type_allocation = self.get_progression_type_allocation()
            self.progression_type = prog_type_allocation.progression_type
            self.min_reps = prog_type_allocation.min_reps
            self.max_reps = prog_type_allocation.max_reps
            self.min_rir = prog_type_allocation.min_rir
            self.max_rir = prog_type_allocation.max_rir
        except:
            self.progression_type = None

    def get_progression_type(self):
        return self.get_progression_type_allocation().progression_type

    def get_progression_type_allocation(self):
        return ProgressionTypeAllocation.objects.get(
            training_focus=self.user.training_focus,
            mechanic=self.mechanic,
            tier=self.tier
        )

    def set_exercise_to_users(self):
        """
        Sets the exercise to all users
        """
        User = apps.get_model('accounts.User')
        users = User.objects.all()
        for user in users:
            if not self.user_has_exercise(user):
                self.id = None
                self.user = user
                self.save()

    def user_has_exercise(self, user):
        """
        Returns True if the user has the exercise
        """
        try:
            Exercise.objects.get(user=user, name=self.name)
            return True
        except:
            return False

    def has_user(self):
        """
        Returns True if the exercise has a user
        """
        return self.user is not None

    def is_new(self):
        """
        Returns True if the exercise is new
        """
        return self.pk is None

    # TODO - add as manager method
    # def get_user_or_null(self):
    #     return Exercise.objects.filter(
    #         Q(user=self.user) | Q(user__isnull=True))


class UserRM(models.Model):
    """
    All of the User's One-Rep-Maxes for specific Exercises.
    Set by save() method of routines.WorkoutExerciseSet.
    """

    # TODO CHANGE TO WEIGHT * REPS @ RIR to track rep-maxes more accurately

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    one_rep_max = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.exercise} - {self.date}'

    objects = models.Manager()
    manager = UserRMManager()
