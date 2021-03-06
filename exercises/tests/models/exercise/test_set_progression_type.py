"""
GIVEN an exercise and user
AND the exercise has progression_type = null
AND the user has a training_focus
WHEN the exercise is saved
THEN the exercise should be allocated a progression_type

need to set progression type when creating exercise for user
exercise has progression type based on
user.training_focus
exercise.mechanic
exercise.tier
exercise.progression_type
lookup reps/rir to progression table
"""

from django.test import TestCase
from exercises.tests.models.factory import ExerciseFactory, MechanicFactory, ProgressionTypeAllocationFactory, TierFactory, ProgressionTypeFactory
from accounts.tests.models.factory import TrainingFocusFactory, UserFactory
from exercises.models import Exercise, ProgressionTypeAllocation


class TestSetProgressionType(TestCase):
    def setUp(self):
        self.training_focus = TrainingFocusFactory()

        self.mechanic = MechanicFactory()
        self.tier = TierFactory()
        self.progression_type = ProgressionTypeFactory()
        self.progression_type_allocation = ProgressionTypeAllocationFactory(
            training_focus=self.training_focus,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.progression_type,
            min_reps=8,
            max_reps=12,
            min_rir=1,
            max_rir=3
        )

    def test_e2e_set_progression_type(self):
        self.user = UserFactory(
            training_focus=self.training_focus
        )

        self.exercise = ExerciseFactory(
            user=self.user,
            mechanic=self.mechanic,
            tier=self.tier
        )

        self.assertEqual(self.exercise.min_reps, 8)
        self.assertEqual(self.exercise.max_reps, 12)
        self.assertEqual(self.exercise.min_rir, 1)
        self.assertEqual(self.exercise.max_rir, 3)

    def test_e2e_user_already_has_progression_type(self):
        """
        GIVEN user has overwritten the progression type 
        AND min/max reps/rir
        WHEN the exercise is saved
        THEN the exercise attributes shouldn't be overwritten
        """
        self.user = UserFactory(
            training_focus=self.training_focus
        )

        self.exercise = ExerciseFactory(
            user=self.user,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.progression_type,
            min_reps=10,
            max_reps=20,
            min_rir=2,
            max_rir=4
        )

        self.assertEqual(self.exercise.min_reps, 10)
        self.assertEqual(self.exercise.max_reps, 20)
        self.assertEqual(self.exercise.min_rir, 2)
        self.assertEqual(self.exercise.max_rir, 4)

    def test_unit_has_progression_type(self):
        self.user = UserFactory(
            training_focus=self.training_focus
        )

        self.exercise = Exercise(
            name='test',
            user=self.user,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.progression_type
        )

        self.assertTrue(self.exercise.has_progression_type())

    def test_unit_set_progression_type(self):
        self.user = UserFactory(
            training_focus=self.training_focus
        )
        self.exercise = Exercise(
            name='test',
            user=self.user,
            mechanic=self.mechanic,
            tier=self.tier
        )

        self.exercise.set_progression_type()
        self.assertEqual(self.exercise.progression_type, self.progression_type)

    def test_unit_get_progression_type(self):
        self.user = UserFactory(
            training_focus=self.training_focus
        )

        self.exercise = Exercise(
            name='test',
            user=self.user,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.progression_type
        )

        self.assertEqual(self.exercise.get_progression_type(),
                         self.progression_type)

    def test_unit_get_progression_type_allocation(self):
        self.user = UserFactory(
            training_focus=self.training_focus
        )

        self.exercise = Exercise(
            name='test',
            user=self.user,
            mechanic=self.mechanic,
            tier=self.tier
        )

        self.assertEqual(
            self.exercise.get_progression_type_allocation(),
            self.progression_type_allocation
        )
