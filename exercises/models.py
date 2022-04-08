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
    training_focus = models.ForeignKey(
        "accounts.TrainingFocus", on_delete=models.CASCADE, null=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(
        ProgressionType, on_delete=models.CASCADE, null=True)
    min_reps = models.PositiveIntegerField(null=True)
    max_reps = models.PositiveIntegerField(null=True)
    target_rir = models.PositiveIntegerField(null=True)
    min_rir = models.PositiveIntegerField(null=True, default=1)

    def __str__(self):
        return f'{self.training_focus}, {self.mechanic}, {self.tier}, {self.progression_type}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['training_focus', 'mechanic', 'tier'], name="UniqueProgressionTypeCheck")
        ]


class Progression(models.Model):
    """
    Lookup table to see how much to change reps/rir for the next set
    Lookup progression_type, rep_delta, rir_delta
    """
    progression_type = models.ForeignKey(
        ProgressionType, on_delete=models.CASCADE)
    rep_delta = models.IntegerField()
    rir_delta = models.IntegerField()
    weight_change = models.FloatField(null=True, blank=True)
    rep_change = models.IntegerField(null=True, blank=True)
    rir_change = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['progression_type', 'rep_delta', 'rir_delta'], name="UniqueProgressionCheck")
        ]


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
    user = models.ForeignKey("accounts.User",
                             on_delete=models.CASCADE, null=True, blank=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True)
    force = models.ForeignKey(Force, on_delete=models.CASCADE, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)
    progression_type = models.ForeignKey(
        ProgressionType, on_delete=models.CASCADE, null=True, blank=True)
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
        return f'{self.name} - {self.user}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.user is None:
            self.set_exercise_to_users()

        # if self.user:
        #     self.set_progression_type()
        #     self.set_min_max_reps()

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

    def set_progression_type(self):
        try:
            self.progression_type = self.get_progression_type()
            self.save()
        except:
            pass

    def set_min_max_reps(self):
        try:
            self.min_reps = self.get_progression_type_allocation().min_reps
            self.max_reps = self.get_progression_type_allocation().max_reps
            self.save()
        except:
            pass

    def get_progression_type_allocation(self):
        try:
            return ProgressionTypeAllocation.objects.get(
                training_focus=self.user.training_focus,
                mechanic=self.mechanic,
                tier=self.tier
            )
        except:
            return None

    def get_progression_type(self):
        try:
            return self.get_progression_type_allocation().progression_type
        except:
            return None


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
