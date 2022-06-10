"""
GIVEN a workout_exercise_set
and workout_exercise.is_set_generate = True
WHEN the workout_exercise_set is created
AND the workout_exercise_set is not within rep range
AND the workout_exercise_set is not within RIR range
THEN the following set should be created
"""

from django.test import TestCase
from accounts.tests.models.factory import UserFactory
from exercises.models import Exercise
from exercises.tests.models.factory import ExerciseFactory

from routines.models import WorkoutExerciseSet
from routines.tests.models.factory import WorkoutExerciseFactory, WorkoutExerciseSetFactory, WorkoutFactory


class TestSetGenerate(TestCase):
    def setUp(self):
        self.user = UserFactory()

        self.exercise = ExerciseFactory(
            user=self.user,
            min_reps=8,
            max_reps=10,
            min_rir=1,
            max_rir=3
        )

        self.workout = WorkoutFactory(user=self.user)
        self.workout_exercise = WorkoutExerciseFactory(
            workout=self.workout,
            exercise=self.exercise,
        )

    def test_e2e_set_generate(self):
        self.workout_exercise_set = WorkoutExerciseSet.objects.create(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        next_set = WorkoutExerciseSet.objects.get(id=2)

        self.assertTrue(next_set.weight == 90)
        self.assertTrue(next_set.reps == None)
        self.assertTrue(next_set.rir == 2)
