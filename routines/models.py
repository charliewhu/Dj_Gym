import math
import decimal

from django.db import models
from accounts.models import User, UserRM
from exercises.models import Exercise, MuscleGroup
from routines.managers import ReadinessAnswerManager


class ReadinessQuestion(models.Model):
    name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return f'{self.name}'


class Readiness(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.date_created}'

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            # only runs on Readiness creation
            Workout.objects.create(user=self.user, readiness=self)

    def percentage(self):
        set = self.readinessanswer_set.all()
        readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        readiness_sum = round(readiness*20) #percentage
        return readiness_sum


class ReadinessAnswer(models.Model):
    class Rating(models.IntegerChoices):
        POOREST = 1
        POORER  = 2
        MEDIUM  = 3
        BETTER  = 4
        BEST    = 5

    readiness          = models.ForeignKey(Readiness, on_delete=models.CASCADE, null=True, blank=True)
    readiness_question = models.ForeignKey(ReadinessQuestion, on_delete=models.CASCADE, null=True, blank=True)
    rating             = models.IntegerField(choices=Rating.choices)

    def __str__(self):
        return f'{self.readiness} - {self.readiness_question}'

    objects = models.Manager()
    manager = ReadinessAnswerManager()


class Workout(models.Model):
    """User's Workout. Contains WorkoutExercises"""
    user         = models.ForeignKey(User, related_name='workouts', on_delete=models.CASCADE, null=True)
    readiness    = models.OneToOneField(Readiness, on_delete=models.CASCADE, null=True)
    date         = models.DateField(auto_now_add=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active    = models.BooleanField(default=1)
    
    def __str__(self):
        str = self.date_created.strftime("%Y-%m-%d - %H:%M:%S")
        return f'{str}'

    def exertion_load(self):
        el = 0
        for exercise in self.exercises.all():
            el += exercise.exertion_load()
        return el
    
    def end_workout(self):
        self.is_active = False
        self.save()


class WorkoutExercise(models.Model):
    workout      = models.ForeignKey(Workout, related_name="exercises", on_delete=models.CASCADE)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, null=True)
    exercise     = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_set_adjust= models.BooleanField(default=0)

    def __str__(self):
        return f'{self.exercise} + {self.workout.date}'

    def exertion_load(self):
        el = 0
        for set in self.sets.all():
            el += set.exertion_load()
        return el


class WorkoutExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name="sets", on_delete=models.CASCADE)
    reps             = models.PositiveIntegerField(blank=True, null=True)
    weight           = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    rir              = models.PositiveIntegerField(blank=True, null=True) 

    def __str__(self):
        return f'{self.workout_exercise} - {self.reps} x {self.weight}kg @{self.rir}RIR'

    def e_one_rep_max(self):
        #calculate the estimated 1RM for that exercise for that set
        reps_divider = decimal.Decimal(self.reps/30)
        rm = self.weight * (1 + reps_divider)
        rrm = round(rm)
        return rrm
        
    def save(self, *args, **kwargs):
        user = self.workout_exercise.workout.user
        exercise = self.workout_exercise.exercise
        rm = self.e_one_rep_max()
        user_rm = UserRM(user=user, exercise=exercise, one_rep_max=rm)
        user_rm.save()
        return super().save(*args, **kwargs)

    def exertion_load(self):
        """Total exertion load for a set"""
        el = 0
        for i in range(self.reps):
            el += math.exp(-0.215 * (self.rir + self.reps - i))
        el = decimal.Decimal(el) * self.weight
        return round(el, 1)
