from os import read
import decimal
from django.db.utils import IntegrityError
from django.test import TestCase
from accounts.tests.models.factory import UserFactory
from exercises.models import Exercise, Progression, ProgressionType, ProgressionTypeAllocation

from routines.models import Readiness, ReadinessAnswer, ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet
from accounts.models import User
from routines.tests.models.factory import ReadinessFactory, WorkoutExerciseFactory, WorkoutExerciseSetFactory, WorkoutFactory
from exercises.tests.models.factory import ProgressionFactory, ProgressionTypeFactory


class WorkoutExerciseSetTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.readiness = ReadinessFactory(user=self.user)
        self.prog_type = ProgressionTypeFactory()
        self.prog_type_allocation = ProgressionTypeAllocation.objects.create(
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            target_rir=3,
            min_rir=2
        )

        self.progression = ProgressionFactory(
            progression_type=self.prog_type,
            rep_delta=0,
            rir_delta=-2,
            weight_change=0.5,
            rep_change=2,
        )
        self.exercise = Exercise.objects.create(
            name="Squat",
            user=self.user,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
        )

        self.workout = WorkoutFactory(user=self.user)
        self.workout_exercise = WorkoutExerciseFactory(
            workout=self.workout,
            exercise=self.exercise
        )
        self.set1 = WorkoutExerciseSetFactory(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=1,
            rir=0
        )

        self.set2 = WorkoutExerciseSetFactory(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=2,
            rir=5
        )

        self.set3 = WorkoutExerciseSetFactory(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=None,
            rir=2,
        )

    def test_exertion_load(self):
        self.assertEqual(self.set1.exertion_load(), 100.0)

    def test_rep_delta(self):
        set1 = WorkoutExerciseSetFactory(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=1,
            rir=0
        )
        self.assertEqual(set1.rep_delta(), 0)

    def test_rir_delta(self):
        self.assertEqual(self.set1.rir_delta(), -2)

    def test_e_one_rep_max(self):
        self.assertEqual(self.set1.e_one_rep_max(), 103)

    def test_get_exercise(self):
        self.assertEqual(self.set1.get_exercise(), self.exercise)

    def test_get_exercise_progression_type(self):
        self.assertEqual(
            self.set1.get_exercise_progression_type(), self.prog_type)

    def test_get_next_set(self):
        self.assertEqual(self.set1.get_next_set(), self.set2)

    def test_is_set_completed(self):
        self.assertTrue(self.set1.is_set_completed(self.set1))
        self.assertTrue(self.set1.is_set_completed(self.set2))
        self.assertFalse(self.set1.is_set_completed(self.set3))

    def test_is_next_set_completed(self):
        self.assertTrue(self.set1.is_next_set_completed())
        self.assertFalse(self.set2.is_next_set_completed())

    def test_should_generate_next_set(self):
        self.assertFalse(self.set1.should_generate_next_set())

    def test_get_progression(self):
        self.assertEqual(self.set1.get_progression(), self.progression)
        self.assertEqual(self.set2.get_progression(), None)

    def test_delete_next_set(self):
        self.assertEqual(WorkoutExerciseSet.objects.count(), 3)
        self.set2.delete_next_set()
        self.assertEqual(WorkoutExerciseSet.objects.count(), 2)

    # TODO - add tests for a WorkoutExercise which has is_set_adjust=True
