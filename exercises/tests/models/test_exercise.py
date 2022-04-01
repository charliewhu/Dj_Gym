from os import read
import decimal
from django.db.utils import IntegrityError
from django.test import TestCase
from exercises.models import Exercise, Mechanic, Progression, ProgressionType, ProgressionTypeAllocation, Purpose, Tier

from accounts.models import FrequencyAllocation, Split, TrainingFocus, User


class ExerciseTest(TestCase):

    def setUp(self):

        self.split = Split.objects.create(
            name="Split",
        )

        self.training_focus = TrainingFocus.objects.create(
            name="Bodybuilding",
        )

        self.frequency_allocation = FrequencyAllocation.objects.create(
            training_focus=self.training_focus,
            training_days=4,
            hierarchy=1,
            split=self.split
        )

        self.user_a = User.objects.create_superuser(
            email='test@test.com',
            password='some_123_password',
        )

        self.user_a.training_focus = self.training_focus
        self.user_a.save()

        self.tier = Tier.objects.create(
            name='T1'
        )

        self.purpose = Purpose.objects.create(
            name='Squat'
        )

        self.mechanic = Mechanic.objects.create(
            name='Compound'
        )

        self.prog_type = ProgressionType.objects.create(
            name='Test',
        )

        self.prog_type_allocation = ProgressionTypeAllocation.objects.create(
            training_focus=self.user_a.training_focus,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            target_rir=3,
            min_rir=2
        )

        self.progression = Progression.objects.create(
            progression_type=self.prog_type,
            rep_delta=0,
            rir_delta=-2,
            weight_change=0.5,
            rep_change=2,
        )

        self.exercise = Exercise.objects.create(
            name="Squat",
            user=self.user_a,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            mechanic=self.mechanic,
            tier=self.tier,
        )

    def test_get_progression_type_allocation(self):
        self.assertEqual(
            self.exercise.get_progression_type_allocation(), self.prog_type_allocation
        )

    def test_get_progression_type(self):
        self.assertEqual(
            self.exercise.get_progression_type(), self.prog_type)

    def test_set_progression_type(self):
        self.exercise2 = Exercise(
            name="Squat",
            user=self.user_a,
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
        )
