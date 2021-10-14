from django.db import models
from django.db.models.fields import DateField
from accounts.models import User


class CycleType(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

# class Routine(models.Model):
#     user        = models.ForeignKey(User, on_delete=models.CASCADE)
#     cycle_type  = models.ForeignKey(CycleType, on_delete=models.CASCADE)
#     start_date  = models.DateField()
#     number      = models.PositiveIntegerField(blank=True, null=True)
#     def __str__(self):
#         return f'{self.user} - {self.cycle_type}, Started on: {self.start_date}'

# class RoutineWeek(models.Model):
#     routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
#     number  = models.PositiveIntegerField()
#     name    = models.CharField(max_length=40, blank=True, null=True)
#     def __str__(self):
#         return self.name

class Workout(models.Model):
    # routine_week    = models.ForeignKey(RoutineWeek, on_delete=models.CASCADE)
    # number          = models.PositiveIntegerField()
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name            = models.CharField(max_length=40, null=True)
    date            = models.DateField(null=True)
    date_created    = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.date} - {self.name}'


class MuscleGroup(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Exercise(models.Model):
    muscle_group    = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    name            = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return f'{self.name}'


class WorkoutItem(models.Model):
    muscle_group    = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, null=True)
    workout         = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise        = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets            = models.PositiveIntegerField(blank=True, null=True)
    reps            = models.PositiveIntegerField(blank=True, null=True)
    weight          = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    rir             = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return f'{self.exercise} - {self.sets} x {self.reps} x {self.weight}kg @{self.rir}RIR'