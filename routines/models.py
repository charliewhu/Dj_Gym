from datetime import datetime
import math
import decimal

from django.db import models
from django.db.models.fields import DateField
from accounts.models import User
from exercises.models import Exercise, MuscleGroup


class Workout(models.Model):
    """User's Workout. Contains WorkoutExercises"""
    user         = models.ForeignKey(User, related_name='workouts', on_delete=models.CASCADE, null=True)
    date         = models.DateField(auto_now_add=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active    = models.BooleanField(default=1)
    
    def end_workout(self):
        self.is_active = False
        self.save()

    def readiness(self):
        """Overall readiness as a percentage"""
        set = self.readiness_set.all()
        readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        return round(readiness*20)

    def squat_readiness(self):
        """Readiness for Squat as a percentage"""
        set = self.readiness_set.all()
        ovr_readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        ex_sum = self.readiness_set\
                .filter(readiness_question__name__icontains='Squat')\
                .aggregate(avg=models.Avg('rating'))['avg']
        combined_readiness = (ex_sum + ovr_readiness) / 2
        return round(combined_readiness * 20)

    def bench_readiness(self):
        """Readiness for Bench as a percentage"""
        set = self.readiness_set.all()
        ovr_readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        ex_sum = self.readiness_set\
                .filter(readiness_question__name__icontains='Bench')\
                .aggregate(avg=models.Avg('rating'))['avg']
        combined_readiness = (ex_sum + ovr_readiness) / 2
        return round(combined_readiness * 20)

    def deadlift_readiness(self):
        """Readiness for Deadlift as a percentage"""
        set = self.readiness_set.all()
        ovr_readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        ex_sum = self.readiness_set\
                .filter(readiness_question__name__icontains='Deadlift')\
                .aggregate(avg=models.Avg('rating'))['avg']
        combined_readiness = (ex_sum + ovr_readiness) / 2
        return round(combined_readiness * 20)

    def pull_readiness(self):
        """Readiness for Pull as a percentage"""
        set = self.readiness_set.all()
        ovr_readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        ex_sum = self.readiness_set\
                .filter(readiness_question__name__icontains='Upper Back')\
                .aggregate(avg=models.Avg('rating'))['avg']
        combined_readiness = (ex_sum + ovr_readiness) / 2
        return round(combined_readiness * 20)

    def __str__(self):
        str = self.date_created.strftime("%Y-%m-%d - %H:%M:%S")
        return f'{str}'


class WorkoutExercise(models.Model):
    workout      = models.ForeignKey(Workout, on_delete=models.CASCADE)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, null=True)
    exercise     = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.exercise} + {self.workout.date}'

    def exercise_exertion_load(self):
        """Must be the sum of set_exertion_load on all child sets"""
        pass 


class WorkoutExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    reps             = models.PositiveIntegerField(blank=True, null=True)
    weight           = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    rir              = models.PositiveIntegerField(blank=True, null=True) 

    def __str__(self):
        return f'{self.workout_exercise} - {self.reps} x {self.weight}kg @{self.rir}RIR'
    
    def set_exertion_load(self):
        """Total exertion load for a set"""
        el = 0
        for i in range(self.reps):
            el += math.exp(-0.215 * (self.rir + self.reps - i))
        el = decimal.Decimal(el) * self.weight
        return round(el, 1)


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


class Readiness(models.Model):
    class Rating(models.IntegerChoices):
        POOREST = 1
        POORER  = 2
        MEDIUM  = 3
        BETTER  = 4
        BEST    = 5

    workout            = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True, blank=True)
    readiness_question = models.ForeignKey(ReadinessQuestion, on_delete=models.CASCADE, null=True, blank=True)
    rating             = models.IntegerField(choices=Rating.choices)

    def __str__(self):
        return f'{self.workout}'

