from datetime import datetime
import math
import decimal

from accounts.models import SplitDay
from .utils import rounder, get_1rm_percent, get_1rm

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Avg

from exercises.models import Exercise, MuscleGroup, Progression, ProgressionTypeAllocation, Rir, UserRM
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
    date         = models.DateField(auto_now_add=True, blank=True)
    split_day    = models.ForeignKey(SplitDay, on_delete=models.CASCADE, null=True, blank=True)
    is_active    = models.BooleanField(default=1)
    is_exercise_generate = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.id} - {self.user} - {self.date}'

    def save(self, *args, **kwargs):
        self.assign_training_day()
        super().save(*args, **kwargs)
        self.create_exercises()

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
                    exercises = force.force.exercise_set.filter(user=self.user) #TODO Force model method
                    exercises = exercises.exclude(id__in=prev_exercises)
                    exercise = exercises.order_by('tier').first()

                    if exercise:
                        WorkoutExercise.objects.create(
                            workout = self,
                            exercise = exercise,
                            is_set_adjust = False,
                            is_set_generate = False
                        )

    def assign_training_day(self):
        try:
            #TODO this should be a manager method
            total_split_days = SplitDay.objects.filter(split_item__split=self.user.split).count() 
            prev_split_day_order = self.last_split_day().order
            this_split_day_num = (prev_split_day_order % total_split_days) + 1
            self.split_day = SplitDay.objects.get(
                split_item__split=self.user.split,
                order = this_split_day_num
            )
        except:
            # If user has no previous workout
            # Or changed TrainingSplit, assign random day
            self.split_day = SplitDay.objects.filter(split_item__split=self.user.split).first()

    def exertion_load(self):
        el = 0
        for exercise in self.exercises.all():
            el += exercise.exertion_load()
        return el

    def last_split_day(self):
        return Workout.objects.filter(user=self.user).last().split_day

    def prev_split_day(self):
        return Workout.objects\
            .filter(split_day__split_item = self.split_day.split_item, user=self.user)\
            .exclude(pk = self.id)\
            .last()

    def prev_split_day_exercises(self):
        return self.prev_split_day().exercises.all()
    
    def end_workout(self):
        self.is_active = False
        self.save()


class WorkoutExercise(models.Model):
    workout         = models.ForeignKey(Workout, related_name="exercises", on_delete=models.CASCADE)
    exercise        = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_set_adjust   = models.BooleanField(default=0)
    is_set_generate = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.workout} - {self.exercise}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_set_generate:
            self.generate_sets()

    def generate_sets(self):

        ## TODO what if user doesnt have a 1rm?        
        one_rm = UserRM.manager.latest_one_rm(self.workout.user, self.exercise)

        pta = self.exercise.get_progression_type_allocation()

        reps = self.exercise.max_reps

        ## TODO create manager on RIR Model for this
        percentage = Rir.objects.get(
            rir = pta.target_rir,
            reps = reps,
            ).percent

        weight = rounder(one_rm * percentage, 2.5)

        for r in range(4):
            WorkoutExerciseSet.objects.create(
                workout_exercise = self,
                weight = weight,
                reps = reps,
            )

    def set_count(self):
        return self.sets.count()

    def avg_reps(self):
        return self.sets.aggregate(Avg('reps'))['reps__avg']
        
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

        """
            only generate next_set if:
                - User chooses set_adjust
                - Set is complete (has weight + reps + rir)
        """
        if self.workout_exercise.is_set_adjust and self.check_set_completed(self):
            self.generate_next_set(exercise)

        
    def following_set(self):
        ## TODO create manager method on WorkoutExerciseSet for this
        next_set = WorkoutExerciseSet.objects\
            .filter(workout_exercise=self.workout_exercise)\
            .filter(id__gt=self.id)\
            .order_by('id')\
            .first()
        return next_set
    
    @staticmethod
    def check_set_completed(set):
        """ Check if the set is completed (has all fields not None)
        Returns (Boolean)"""
        return set.weight is not None \
            and set.reps \
            and set.rir is not None

    def generate_next_set(self, exercise):
        """
        Generate another set based on the current instance:
            - Lookup to Progression
            - Adjust weight/reps/rir based on Progression
            - Create another WorkoutExerciseSet object
        """
        
        # when updating: check if user has completed following set
        # if not, delete() 
        # then proceed to regenerate
        next_set = self.following_set()
        if next_set and not self.check_set_completed(next_set):
            id = next_set.id
            next_set.delete()
        
        rep_d = self.rep_delta()
        rir_d = self.rir_delta()
        try:
            prog = Progression.objects.get(
                progression_type = exercise.progression_type,
                rep_delta = rep_d,
                rir_delta = rir_d
                )
        except:
            prog = None

        if prog:
            if prog.weight_change is not None:
                next_weight = rounder(float(self.weight) * (1 + prog.weight_change), 2.5)
            else:
                next_weight = None

            if prog.rep_change is not None:
                next_reps = self.reps + prog.rep_change
            else:
                next_reps = None
            
            if prog.rir_change is not None:
                next_rir = self.rir + prog.rir_change
            else: 
                next_rir = None

            WorkoutExerciseSet.objects.create(
                id = id,
                workout_exercise = self.workout_exercise,
                weight = next_weight,
                reps = next_reps,
                rir = next_rir
            )
    
    def rep_delta(self):
        """difference between reps just done and required rep range"""
        prog_type = self.workout_exercise.exercise.progression_type
        if self.reps < prog_type.min_reps:
            rep_delta = self.reps - prog_type.min_reps
        elif self.reps > prog_type.max_reps:
            rep_delta = self.reps - prog_type.max_reps
        else:
            rep_delta = 0

        return rep_delta

    def rir_delta(self):
        """difference between rir just done and required rir range"""
        prog_type = self.workout_exercise.exercise.progression_type
        if self.rir < prog_type.min_rir:
            rir_delta = self.rir - prog_type.min_rir
        elif self.rir > prog_type.target_rir:
            rir_delta = self.rir - prog_type.target_rir
        else:
            rir_delta = 0

        return rir_delta

    def e_one_rep_max(self):
        #calculate the estimated 1RM for that exercise for that set
        """
        Change to use RIR table for E1RM instead of formular
        """
        reps_divider = self.reps/30
        rm = float(self.weight) * (1 + reps_divider)
        rounded_rm = round(rm)
        return rounded_rm

    def save_one_rep_max(self, user, exercise):
        if self.rir and self.reps and self.weight:
            if self.rir < 5 and self.reps <= 10: ## only set 1rm on hard sets
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
            el += math.exp(-0.215 * (self.rir + self.reps - (i+1)))
        el = decimal.Decimal(el) * self.weight
        return round(el, 1)