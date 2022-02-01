from django.db import models
from accounts.models import User, UserProfile
from .managers import UserRMManager


class Rir(models.Model):
    rir = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    percent = models.FloatField()


class Force(models.Model):
    """eg Hip Hinge, Vertical Push"""
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

class Tier(models.Model):
    #tier_choices = (('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('Other', 'Other'),)
    name =  name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Purpose(models.Model):
    # purpose_choices = (('Squat', 'Squat'),('Bench', 'Bench'),('Deadlift', 'Deadlift'),)
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Mechanic(models.Model):
    #mechanic_choices = (('Compound', 'Compound'), ('Isolation', 'Isolation'))
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name  = models.CharField(max_length=20, unique=True)
    force = models.ManyToManyField(Force)
    
    def __str__(self):
        return self.name


class ProgressionType(models.Model):
    name     = models.CharField(max_length=40, unique=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    purpose  = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True)
    force    = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    tier     = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    ## need constraints on combinations of mech/pur/force/tier


class Exercise(models.Model):
    name = models.CharField(max_length=60, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    force = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(ProgressionType, on_delete=models.CASCADE, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True,
        help_text="Which powerlifting exercise does this improve?")
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True,
        help_text="T1 exercises are the competition exercises.\
            T2 exercises are close variations of the main lifts. \
            T3 exercises develop the musculature eg. quads for squats. \
            Other exercises develop supplementary muscles")
    # User should see exercises where user is NULL (mixed exercises)
    # and where user==currentUser

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name="UserUniqueExercise")
            ]

    def __str__(self):
        return self.name
    


class UserRM(models.Model):
    """
    All of the User's One-Rep-Maxes for specific Exercises.
    Set by the User until they expire or are beaten.
    """

    ## CHANGE TO WEIGHT * REPS @ RIR to track rep-maxes more accurately

    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    one_rep_max = models.PositiveIntegerField()
    date        = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.exercise} - {self.date}'

    objects = models.Manager()
    one_rm_manager = UserRMManager()