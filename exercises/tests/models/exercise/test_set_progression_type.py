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
from exercises.tests.models.factory import ExerciseFactory, MechanicFactory, TierFactory, ProgressionTypeFactory
from accounts.tests.models.factory import TrainingFocusFactory, UserFactory


class TestSetProgressionType(TestCase):
    def setUp(self):
        self.training_focus = TrainingFocusFactory()
        self.user = UserFactory(
            training_focus=self.training_focus
        )

        self.mechanic = MechanicFactory()
        self.tier = TierFactory()
        self.progression_type = ProgressionTypeFactory()
        self.progression_type_allocation = ProgressionTypeAllocation(
            training_focus=self.training_focus,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.progression_type
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
        )
