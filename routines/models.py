from datetime import datetime
import math
import decimal

from accounts.models import SplitDay
from .utils import rounder, get_1rm_percent, get_1rm

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

from exercises.models import Exercise, MuscleGroup, Rir, UserRM
from routines.managers import ReadinessAnswerManager


class ReadinessQuestion(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True)

    def __str__(self):
        return f'{self.name}'


class Readiness(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)
    date_created = models.DateField(
        auto_now_add=True,
        null=True)

    def __str__(self):
        return f'{self.date_created}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            # create associated Workout instance
            Workout.objects.create(user=self.user, readiness=self)
        except:
            pass

    def get_workout(self):
        return Workout.objects.get(readiness=self)

    def percentage(self):
        set = self.readinessanswer_set.all()
        readiness = set.aggregate(avg=models.Avg('rating'))['avg']
        readiness_sum = round(readiness*20)  # percentage
        return readiness_sum


class ReadinessAnswer(models.Model):
    class Rating(models.IntegerChoices):
        POOREST = 1
        POORER = 2
        MEDIUM = 3
        BETTER = 4
        BEST = 5

    readiness = models.ForeignKey(
        Readiness, on_delete=models.CASCADE, null=True, blank=True)
    readiness_question = models.ForeignKey(
        ReadinessQuestion, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=Rating.choices)

    def __str__(self):
        return f'{self.readiness.user} - {self.readiness} - {self.readiness_question}'

    objects = models.Manager()
    manager = ReadinessAnswerManager()


class Workout(models.Model):
    """User's Workout. Contains WorkoutExercises"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='workouts', on_delete=models.CASCADE, null=True)
    readiness = models.OneToOneField(
        Readiness, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, blank=True)
    split_day = models.ForeignKey(
        SplitDay, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=1)
    is_exercise_generate = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.id} - {self.user} - {self.date}'

    def save(self, *args, **kwargs):
        # self.assign_training_day()
        super().save(*args, **kwargs)
        # self.create_exercises()

    def create_exercises(self):
        """
        Create WorkoutExercise for the first in each Force
        Excluding those that appeared in the prev Workout with the same SplitItem
        """
        prev_exercises = self.prev_split_day_exercises().values_list("exercise", flat=True)
        forces = self.split_day.splitdayforce_set.all().order_by('hierarchy')
        if not self.exercises.all():
            if self.is_exercise_generate:
                for force in forces:
                    exercises = force.force.exercise_set.filter(
                        user=self.user)  # TODO Force model method
                    exercises = exercises.exclude(id__in=prev_exercises)
                    exercise = exercises.order_by('tier').first()

                    if exercise:
                        WorkoutExercise.objects.create(
                            workout=self,
                            exercise=exercise,
                            is_set_adjust=False,
                            is_set_generate=False
                        )

    def assign_training_day(self):
        try:
            # TODO this should be a manager method
            total_split_days = self.user.split_days_count()
            prev_split_day_order = self.last_split_day().order
            this_split_day_num = (prev_split_day_order % total_split_days) + 1
            self.split_day = SplitDay.objects.get(
                split_item__split=self.user.split,
                order=this_split_day_num
            )
        except:
            # If user has no previous workout
            # Or changed TrainingSplit, assign random day
            self.split_day = SplitDay.objects.filter(
                split_item__split=self.user.split).first()

    def exertion_load(self):
        el = 0
        for exercise in self.exercises.all():
            el += exercise.exertion_load()
        return el

    def last_split_day(self):
        """
        Input: Workout instance
        Output: The SplitDay of the users previous Workout
        """
        return Workout.objects.filter(user=self.user).last().split_day

    def prev_split_day(self):
        """
        Input: Workout instance
        Output: Users previous Workout instance with the same SplitDay as the input
        """
        if self.last_split_day is not None:
            return Workout.objects\
                .filter(split_day__split_item=self.split_day.split_item, user=self.user)\
                .exclude(pk=self.id)\
                .last()
        return None

    def prev_split_day_exercises(self):
        """
        Input: Workout instance
        Output: WorkoutExercise queryset for the users previous Workout instance 
        with the same SplitDay as the input
        """
        return self.prev_split_day().exercises.all()

    def end_workout(self):
        self.is_active = False
        self.save()


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout, related_name="exercises", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_set_adjust = models.BooleanField(default=0)
    is_set_generate = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.workout} - {self.exercise}'


class WorkoutExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(
        WorkoutExercise, related_name="sets", on_delete=models.CASCADE)
    weight = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True)
    reps = models.PositiveIntegerField(blank=True, null=True)
    rir = models.PositiveIntegerField(
        blank=True, null=True, validators=[MaxValueValidator(5)])

    def __str__(self):
        return f'{self.workout_exercise} - {self.reps} x {self.weight}kg @{self.rir}RIR'

    def save(self, *args, **kwargs):
        # create user-rep-max instance
        super().save(*args, **kwargs)

        if self.should_generate_next_set():
            self.generate_next_set()

    def should_generate_next_set(self):
        return self.workout_exercise.is_set_adjust and self.is_next_set_completed()

    def is_next_set_completed(self):
        """Returns false if next set does not exist 
        or if any field is None"""
        next_set = self.get_next_set()
        if next_set:
            return next_set.is_set_completed()
        else:
            return False

    def generate_next_set(self):
        """
        Generate another set based on the current instance:
            - Get Progression based on current set
            - Adjust weight/reps/rir based on Progression
            - Check if user has a completed next set
                - If true: update it
                - Else: Create another WorkoutExerciseSet object
        """

        pass

    def exertion_load(self):
        """Total exertion load for a set"""
        el = 0
        for i in range(self.reps):
            el += math.exp(-0.215 * (self.rir + self.reps - (i+1)))
        el = decimal.Decimal(el) * self.weight
        return round(el, 1)
