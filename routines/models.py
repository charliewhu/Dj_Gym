from datetime import datetime

from django.db import models
from django.db.models.fields import DateField
from accounts.models import User


class Workout(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date         = models.DateField(auto_now_add=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def readiness(self):
        return self.workoutreadiness_set.all().aggregate(sum=models.Sum('rating'))['sum']

    def __str__(self):
        str = self.date_created.strftime("%Y-%m-%d - %H:%M:%S")
        return f'{str}'


class MuscleGroup(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Exercise(models.Model):
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    name         = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return f'{self.name}'


class WorkoutExercise(models.Model):
    workout      = models.ForeignKey(Workout, on_delete=models.CASCADE)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, null=True)
    exercise     = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.exercise}'


class WorkoutExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    reps             = models.PositiveIntegerField(blank=True, null=True)
    weight           = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    rir              = models.PositiveIntegerField(blank=True, null=True) 

    def __str__(self):
        return f'{self.workout_exercise} - {self.reps} x {self.weight}kg @{self.rir}RIR'


class WorkoutItem(models.Model):
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, null=True)
    workout      = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise     = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets         = models.PositiveIntegerField(blank=True, null=True)
    reps         = models.PositiveIntegerField(blank=True, null=True)
    weight       = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    rir          = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.exercise} - {self.sets} x {self.reps} x {self.weight}kg @{self.rir}RIR'


class ReadinessQuestion(models.Model):
    name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return f'{self.name}'


class WorkoutReadiness(models.Model):
    class Rating(models.IntegerChoices):
        LOWEST  = 1
        LOWER   = 2
        MEDIUM  = 3
        HIGHER  = 4
        HIGHEST = 5

    workout            = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True, blank=True)
    readiness_question = models.ForeignKey(ReadinessQuestion, on_delete=models.CASCADE, null=True, blank=True)
    rating             = models.IntegerField(choices=Rating.choices)

    def __str__(self):
        return f'{self.workout}'





# class WorkoutReadiness(models.Model):
#     class Rating(models.IntegerChoices):
#         LOWEST  = 1
#         LOWER   = 2
#         MEDIUM  = 3
#         HIGHER  = 4
#         HIGHEST = 5

#     workout   = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True, blank=True)
#     sleep     = models.IntegerField(choices=Rating.choices)
#     energy    = models.IntegerField(choices=Rating.choices)
#     mood      = models.IntegerField(choices=Rating.choices)
#     soreness  = models.IntegerField(choices=Rating.choices)
#     stress    = models.IntegerField(choices=Rating.choices)
#     nutrition = models.IntegerField(choices=Rating.choices)
#     hydration = models.IntegerField(choices=Rating.choices)
#     weight    = models.IntegerField()
#     def __str__(self):
#         return f'{self.workout}'
