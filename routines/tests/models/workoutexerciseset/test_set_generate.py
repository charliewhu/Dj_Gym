"""
GIVEN a workout_exercise_set
and workout_exercise.is_set_generate = True
WHEN the workout_exercise_set is created
AND the workout_exercise_set is not within rep range
AND the workout_exercise_set is not within RIR range
AND the next set hasnt already been completed
THEN the following set should be created
"""

from django.test import TestCase
from accounts.tests.models.factory import TrainingFocusFactory, UserFactory
from exercises.models import Exercise, ProgressionTypeAllocation
from exercises.tests.models.factory import ExerciseFactory, ProgressionFactory, ProgressionTypeAllocationFactory

from routines.models import WorkoutExerciseSet
from routines.tests.models.factory import (
    WorkoutExerciseFactory,
    WorkoutFactory
)


class TestSetGenerate(TestCase):
    def setUp(self):
        self.training_focus = TrainingFocusFactory()
        self.user = UserFactory(
            training_focus=self.training_focus
        )
        self.progression = ProgressionFactory(
            rep_delta=0,
            rir_delta=-1,
            weight_change=-0.5,
            rep_change=2
        )
        self.exercise = ExerciseFactory(
            user=self.user,
            progression_type=self.progression.progression_type,
            min_reps=8,
            max_reps=10,
            min_rir=2,
            max_rir=3
        )

        self.progression_type_allocation = ProgressionTypeAllocationFactory(
            training_focus=self.training_focus,
            mechanic=self.exercise.mechanic,
            tier=self.exercise.tier,
            progression_type=self.progression.progression_type,
            min_reps=8,
            max_reps=12,
            min_rir=1,
            max_rir=3
        )

        self.workout = WorkoutFactory(user=self.user)
        self.workout_exercise = WorkoutExerciseFactory(
            workout=self.workout,
            exercise=self.exercise,
            is_set_adjust=True
        )

    def test_e2e_set_generate(self):
        self.workout_exercise_set = WorkoutExerciseSet.objects.create(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=8,
            rir=0
        )

        next_set = self.workout_exercise_set.generate_next_set()

        self.assertTrue(next_set.weight == 50)
        self.assertTrue(next_set.reps == 10)
        self.assertTrue(next_set.rir == None)

    def test_unit_adjust_weight(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=8,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.adjust_weight(self.progression),
            50
        )

    def test_unit_adjust_reps(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=8,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.adjust_reps(self.progression),
            10
        )

    def test_unit_adjust_rir(self):
        self.progression.rir_change = 1
        self.progression.save()
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.adjust_rir(self.progression),
            1
        )

    def test_unit_get_progression(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=8,
            rir=0
        )

        self.assertEqual(
            self.workout_exercise_set.get_progression(),
            self.progression
        )

    def test_unit_get_exercise_progression_type_allocation(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        pta = ProgressionTypeAllocation.objects.get(
            training_focus=self.user.training_focus,
            mechanic=self.exercise.mechanic,
            tier=self.exercise.tier
        )

        self.assertEqual(
            self.workout_exercise_set.get_exercise_progression_type_allocation(),
            pta
        )

    def test_unit_get_rep_delta(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.get_rep_delta(),
            -2
        )

    def test_unit_get_rir_delta(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.get_rir_delta(),
            -1
        )

    def test_unit_get_exercise_progression_type(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.get_exercise_progression_type(),
            self.exercise.progression_type
        )

    def test_unit_get_exercise(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )
        self.assertEqual(
            self.workout_exercise_set.get_exercise(),
            self.exercise
        )

    def test_unit_should_generate_next_set(self):
        """
        GIVEN a workout_exercise_set
        AND .workout_exercise.is_set_generate = True
        AND the wotkout_exercise_set is complete
        AND the next set is not complete or doesnt exist
        WHEN the workout_exercise_set is created
        THEN we should generate the next set
        """
        self.workout_exercise_set = WorkoutExerciseSet.objects.create(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        self.assertTrue(self.workout_exercise_set.should_generate_next_set())

        self.workout_exercise_set2 = WorkoutExerciseSet.objects.create(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=6,
            rir=None
        )

        self.assertFalse(self.workout_exercise_set2.should_generate_next_set())

    def test_unit_is_next_set_completed(self):
        workout_exercise = WorkoutExerciseFactory(
            workout=self.workout,
            exercise=self.exercise,
            is_set_adjust=False
        )
        self.workout_exercise_set = WorkoutExerciseSet.objects.create(
            workout_exercise=workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        self.assertFalse(self.workout_exercise_set.is_next_set_completed())

        self.workout_exercise_set2 = WorkoutExerciseSet.objects.create(
            workout_exercise=workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        self.assertTrue(self.workout_exercise_set.is_next_set_completed())

    def test_unit_get_next_set(self):
        workout_exercise = WorkoutExerciseFactory(
            workout=self.workout,
            exercise=self.exercise,
            is_set_adjust=False
        )

        self.workout_exercise_set = WorkoutExerciseSet.objects.create(
            workout_exercise=workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        self.workout_exercise_set2 = WorkoutExerciseSet.objects.create(
            workout_exercise=workout_exercise,
            weight=100,
            reps=6,
            rir=0
        )

        self.assertEqual(
            self.workout_exercise_set.get_next_set(),
            self.workout_exercise_set2
        )

    def test_unit_is_set_completed(self):
        self.workout_exercise_set = WorkoutExerciseSet(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=None,
            rir=0
        )

        self.assertFalse(self.workout_exercise_set.is_set_completed())

        self.workout_exercise_set.reps = 6
        self.assertTrue(self.workout_exercise_set.is_set_completed())
