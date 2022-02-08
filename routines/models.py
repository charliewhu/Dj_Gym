import math
import decimal
from .utils import rounder, get_1rm_percent, get_1rm

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator

from exercises.models import Exercise, MuscleGroup, Rir, UserRM
from routines.managers import ReadinessAnswerManager


class ReadinessQuestion(models.Model):
    name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return f'{self.name}'


class Readiness(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.date_created}'

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        if not self.pk:
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
        return f'{self.readiness.user} - {self.readiness} - {self.readiness_question}'

    objects = models.Manager()
    manager = ReadinessAnswerManager()


class Workout(models.Model):
    """User's Workout. Contains WorkoutExercises"""
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='workouts', on_delete=models.CASCADE, null=True)
    readiness    = models.OneToOneField(Readiness, on_delete=models.CASCADE, null=True)
    date         = models.DateField(auto_now_add=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active    = models.BooleanField(default=1)
    
    def __str__(self):
        return f'{self.user} - {self.date}'

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
        return f'{self.workout} - {self.exercise}'

    def exertion_load(self):
        el = 0
        for set in self.sets.all():
            el += set.exertion_load()
        return el


class WorkoutExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name="sets", on_delete=models.CASCADE)
    weight           = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    reps             = models.PositiveIntegerField(blank=True, null=True)
    rir              = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(5)]) 

    def __str__(self):
        return f'{self.workout_exercise} - {self.reps} x {self.weight}kg @{self.rir}RIR'

    def save(self, *args, **kwargs):
        #create user-rep-max instance
        user = self.workout_exercise.workout.user
        exercise = self.workout_exercise.exercise
        self.save_one_rep_max(user, exercise)
        super().save(*args, **kwargs)
        self.next_set(user, exercise)
        
    def next_set(self, user, exercise):
        if self.weight and self.reps and self.rir is not None:
            print("Do logic!")
            self.rep_drop(user, exercise)

    def rep_drop(self, user, exercise):
        one_rm = UserRM.one_rm_manager.latest_one_rm(user=user, exercise=exercise) or None
        if exercise.progression_type.name == "Rep-Drop":
            print("in rep-drop block")
            self.rep_drop_no_1rm(exercise)

    def rep_delta(self):
        prog_type = self.workout_exercise.exercise.progression_type
        if self.reps < prog_type.min_reps:
            rep_delta = self.reps - prog_type.min_reps
        elif self.reps > prog_type.max_reps:
            rep_delta = self.reps - prog_type.max_reps
        else:
            rep_delta = 0
        print("Rep Delta: ", rep_delta)
        return rep_delta

    def rir_delta(self):
        prog_type = self.workout_exercise.exercise.progression_type
        if self.rir < prog_type.min_rir:
            rir_delta = self.rir - prog_type.min_rir
        elif self.rir > prog_type.target_rir:
            rir_delta = self.rir - prog_type.target_rir
        else:
            rir_delta = 0
        print("RIR Delta: ",rir_delta)
        return rir_delta

    def rep_drop_no_1rm(self, exercise):
        print("in no 1RM block")
        target_rir = exercise.progression_type.target_rir
        min_reps = exercise.progression_type.min_reps
        max_reps = exercise.progression_type.max_reps
        current_pct = get_1rm_percent(self.reps, self.rir)
        target_pct = get_1rm_percent(min_reps, target_rir)
        pct_change_needed = target_pct / current_pct
        
        if self.reps >= min_reps and self.reps <= max_reps:  # reps fine
            print("reps fine")

            if self.rir > target_rir: # rir easy
                print("low effort")
                next_weight = float(self.weight) * 1.1
                next_weight = rounder(next_weight, 2.5)

                WorkoutExerciseSet.objects.create(
                    workout_exercise = self.workout_exercise,
                    weight = next_weight,
                    rir = target_rir
                )
                
            elif self.rir < target_rir: # rir hard
                print("high effort")
                next_weight = float(self.weight) * 0.9
                next_weight = rounder(next_weight, 2.5)

                WorkoutExerciseSet.objects.create(
                    workout_exercise = self.workout_exercise,
                    weight = next_weight,
                    reps = self.reps
                )
                
            elif self.rir == target_rir:
                print("effort fine")
                WorkoutExerciseSet.objects.create(
                    workout_exercise = self.workout_exercise,
                    weight = self.weight,
                    rir = self.rir
                )

        elif self.reps > max_reps: # reps high
            print("reps high")
            if self.rir > target_rir: # rir easy
                print("low effort")
                next_weight = float(self.weight) * 1.2
                next_weight = rounder(next_weight, 2.5)

                WorkoutExerciseSet.objects.create(
                    workout_exercise = self.workout_exercise,
                    weight = next_weight,
                    rir = target_rir
                )

            elif self.rir < target_rir: # rir hard
                print("high effort")
                next_weight = self.min_new_weight(pct_change_needed, 1.2)
                
                WorkoutExerciseSet.objects.create(
                    workout_exercise = self.workout_exercise,
                    weight = next_weight,
                    rir = target_rir
                )
                
            elif self.rir == target_rir: # rir fine
                print("effort fine")
                pass


    def min_new_weight(self, pct, max_pct):
        w1 = float(self.weight) * pct
        w2 = float(self.weight) * max_pct
        next_weight = min(w1, w2)
        return rounder(next_weight, 2.5)

    def max_new_weight(self, pct, max_pct):
        w1 = float(self.weight) * pct
        w2 = float(self.weight) * max_pct
        next_weight = max(w1, w2)
        return rounder(next_weight, 2.5)

    def e_one_rep_max(self):
        #calculate the estimated 1RM for that exercise for that set
        """
        Change to use RIR table for E1RM instead of formular
        """
        reps_divider = decimal.Decimal(self.reps/30)
        rm = self.weight * (1 + reps_divider)
        rounded_rm = round(rm)
        return rounded_rm

    def save_one_rep_max(self, user, exercise):
        if self.rir and self.reps and self.weight:
            if self.rir < 5 and self.reps <= 10:
                rm = self.e_one_rep_max()
                user_rm = UserRM(
                    user=user, 
                    exercise=exercise, 
                    one_rep_max=rm
                )
                user_rm.save()

    def exertion_load(self):
        """Total exertion load for a set"""
        el = 0
        for i in range(self.reps):
            el += math.exp(-0.215 * (self.rir + self.reps - i))
        el = decimal.Decimal(el) * self.weight
        return round(el, 1)
