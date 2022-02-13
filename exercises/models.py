from django.conf import settings
from django.db import models
from .managers import UserRMManager


class Rir(models.Model):
    rir = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    percent = models.FloatField()


class Force(models.Model):
    """Hip Hinge, Vertical Push etc"""
    name = models.CharField(max_length=60, unique=True)
    base_weekly_sets = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class Tier(models.Model):
    """T1, T2, T3, Other"""
    name =  name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Purpose(models.Model):
    """Squat, Bench, Deadlift"""
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Mechanic(models.Model):
    """Compound, Isolation"""
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name  = models.CharField(max_length=20, unique=True)
    force = models.ManyToManyField(Force)
    
    def __str__(self):
        return self.name


class ProgressionType(models.Model):
    """Top, Straight, Rep-drop, Technique, Ladder, Pyramid"""
    name           = models.CharField(max_length=40, unique=True)
    training_focus = models.ForeignKey("accounts.TrainingFocus", on_delete=models.CASCADE, null=True)
    mechanic       = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    tier           = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    min_reps       = models.PositiveIntegerField(null=True)
    max_reps       = models.PositiveIntegerField(null=True)
    target_rir     = models.PositiveIntegerField(null=True)
    min_rir        = models.PositiveIntegerField(null=True, default=1)

    def __str__(self):
        return f'{self.training_focus}, {self.mechanic}, {self.tier} - {self.name}'

    ## need constraints on combinations of focus/mech/tier


class Progression(models.Model):
    progression_type = models.ForeignKey(ProgressionType, on_delete=models.CASCADE)
    rep_delta        = models.IntegerField()
    rir_delta        = models.IntegerField()
    weight_change    = models.FloatField(null=True, blank=True)
    rep_change       = models.IntegerField(null=True, blank=True)
    rir_change       = models.IntegerField(null=True, blank=True)

    ## need unique constraints on prog_type/rep_delta/rir_delta


class Exercise(models.Model):
    name            = models.CharField(max_length=60)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    mechanic        = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    force           = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    isolation       = models.BooleanField(null=True, default=False)
    progression_type= models.ForeignKey(ProgressionType, on_delete=models.CASCADE, null=True, blank=True)
    purpose         = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True,
        help_text="Which powerlifting exercise does this improve?")
    tier            = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True,
        help_text="T1 exercises are the competition exercises.\
            T2 exercises are close variations of the main lifts. \
            T3 exercises develop the musculature eg. quads for squats. \
            Other exercises develop supplementary muscles")
    is_active       = models.BooleanField(default=1)
    # User should see exercises where user is NULL (mixed exercises)
    # and where user==currentUser

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name="UserUniqueExercise")
            ]

    def __str__(self):
        return f'{self.name} - {self.user}'
    


class UserRM(models.Model):
    """
    All of the User's One-Rep-Maxes for specific Exercises.
    Set by save() method of routines.WorkoutExerciseSet.
    """

    ## CHANGE TO WEIGHT * REPS @ RIR to track rep-maxes more accurately

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    one_rep_max = models.PositiveIntegerField()
    date        = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.exercise} - {self.date}'

    objects = models.Manager()
    one_rm_manager = UserRMManager()