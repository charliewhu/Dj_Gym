from django.conf import settings
from django.db import models

from .managers import UserRMManager


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
    name =  name = models.CharField(max_length=20, unique=True)
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
    """Allocates training focus to exercises depending on User TrainingFocus"""
    training_focus   = models.ForeignKey("accounts.TrainingFocus", on_delete=models.CASCADE, null=True)
    mechanic         = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    tier             = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(ProgressionType, on_delete=models.CASCADE, null=True)
    min_reps         = models.PositiveIntegerField(null=True)
    max_reps         = models.PositiveIntegerField(null=True)
    target_rir       = models.PositiveIntegerField(null=True)
    min_rir          = models.PositiveIntegerField(null=True, default=1)

    def __str__(self):
        return f'{self.training_focus}, {self.mechanic}, {self.tier}, {self.progression_type}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['training_focus', 'mechanic', 'tier'], name="UniqueProgressionTypeCheck")
            ]


class Progression(models.Model):
    progression_type = models.ForeignKey(ProgressionType, on_delete=models.CASCADE)
    rep_delta        = models.IntegerField()
    rir_delta        = models.IntegerField()
    weight_change    = models.FloatField(null=True, blank=True)
    rep_change       = models.IntegerField(null=True, blank=True)
    rir_change       = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['progression_type', 'rep_delta', 'rir_delta'], name="UniqueProgressionCheck")
            ]


class Force(models.Model):
    """Hip Hinge, Vertical Push etc"""
    name             = models.CharField(max_length=60, unique=True)
    base_weekly_sets = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name  = models.CharField(max_length=20, unique=True)
    force = models.ManyToManyField(Force)
    
    def __str__(self):
        return self.name


class Exercise(models.Model):
    name             = models.CharField(max_length=60)
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    mechanic         = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    force            = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    purpose          = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True)
    tier             = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(ProgressionType, on_delete=models.CASCADE, null=True, blank=True)
    min_reps         = models.PositiveIntegerField(null=True, blank=True)
    max_reps         = models.PositiveIntegerField(null=True, blank=True)
    is_active        = models.BooleanField(default=1)
    is_unilateral    = models.BooleanField(default=0)
    # User should see exercises where user is NULL (mixed exercises)
    # and where user==currentUser

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name="UserUniqueExercise")
            ]

    def __str__(self):
        return f'{self.name} - {self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_progression_type()
        ## TODO - If Exercises is added by Admin, all Users should receive the exercise to their libraries
        ## duplicate with every UserID and their progression type
        ## consider if they already have an exercise with this name

    def set_progression_type(self):
        if self.user:
            if not self.progression_type and not self.min_reps and not self.max_reps:
                prog = self.get_progression_type_allocation()
                self.progression_type = prog.progression_type
                self.min_reps = prog.min_reps
                self.max_reps = prog.max_reps
                self.save()

    def get_progression_type_allocation(self):
        print(self.user.training_focus)
        print(self.mechanic)
        print(self.tier)
        return ProgressionTypeAllocation.objects.get(
            training_focus = self.user.training_focus,
            mechanic  = self.mechanic,
            tier = self.tier
        )
    

class UserRM(models.Model):
    """
    All of the User's One-Rep-Maxes for specific Exercises.
    Set by save() method of routines.WorkoutExerciseSet.
    """

    ## TODO CHANGE TO WEIGHT * REPS @ RIR to track rep-maxes more accurately

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    one_rep_max = models.PositiveIntegerField()
    date        = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.exercise} - {self.date}'

    objects = models.Manager()
    manager = UserRMManager()