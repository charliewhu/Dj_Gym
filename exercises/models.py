from django.conf import settings
from django.db import models
from django.apps import apps

from .managers import UserRMManager
from django.db.models import Q


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


class Exercise(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    force = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    min_reps = models.PositiveIntegerField(null=True, blank=True)
    max_reps = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=1)
    is_unilateral = models.BooleanField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="UserUniqueExercise")
        ]

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None
    #     super().save(*args, **kwargs)
    #     if is_new and self.user is None:
    #         self.set_exercise_to_users()

    #     if is_new and self.user:
    #         self.set_progression_type()
    #         self.set_min_max_reps()

    # TODO - add as manager method
    # def get_user_or_null(self):
    #     return Exercise.objects.filter(
    #         Q(user=self.user) | Q(user__isnull=True))

    def set_exercise_to_users(self):
        """
        Sets the exercise to all users
        """
        User = apps.get_model('accounts.User')
        users = User.objects.all()
        for user in users:
            try:
                Exercise.objects.get(
                    user=user, name=self.name)
                user_has_exercise = True
            except:
                user_has_exercise = False

            if not user_has_exercise:
                self.id = None
                self.user = user
                self.save()


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
