from os import read
import decimal
from django.db.utils import IntegrityError
from django.test import TestCase
from exercises.models import Exercise, Force, Mechanic, Progression, ProgressionType, ProgressionTypeAllocation, Purpose, Tier


from accounts.models import FrequencyAllocation, Split, TrainingFocus, User
from exercises.tests.models.factory import ExerciseFactory, MechanicFactory, ProgressionFactory, ProgressionTypeAllocationFactory, ProgressionTypeFactory, PurposeFactory, TierFactory, TrainingFocusFactory
from accounts.tests.models.factory import ForceFactory, FrequencyAllocationFactory, SplitFactory, UserFactory


class ExerciseTest(TestCase):

    def setUp(self):
        
        self.split = SplitFactory()
        self.training_focus = TrainingFocusFactory()
        self.frequency_allocation = FrequencyAllocationFactory(
            split=self.split, 
            training_focus=self.training_focus
        )
        self.user = UserFactory()
        self.force = ForceFactory()
        self.tier = TierFactory()
        self.purpose = PurposeFactory()
        self.mechanic = MechanicFactory()
        self.prog_type = ProgressionTypeFactory()

        self.prog_type_allocation = ProgressionTypeAllocationFactory(
            training_focus=self.user.training_focus,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.prog_type,
        )

        self.progression = ProgressionFactory(
            progression_type=self.prog_type,
        )

        self.exercise = ExerciseFactory(
            name="Squat",
            user=self.user,
            force=self.force,
            purpose=self.purpose,
            mechanic=self.mechanic,
            tier=self.tier,
            progression_type=self.prog_type,
        )

    def test_get_progression_type_allocation(self):
        self.assertEqual(
            self.exercise.get_progression_type_allocation(), self.prog_type_allocation
        )

    def test_get_progression_type(self):
        self.assertEqual(
            self.exercise.get_progression_type(), self.prog_type)

    def test_set_progression_type(self):
        pass

    def test_admin_added_exercise(self):
        # GIVEN an admin user
        # WHEN they add a new exercise
        # AND user is not set
        exercise = Exercise.objects.create(
            name="Squat2",
            user=None,
            mechanic=self.mechanic,
            force=self.force,
            tier=self.tier,
        )
        # THEN the exercise should be copied out to all users
        # AND every user should have a copy of the exercise
        user_exercise = Exercise.objects.get(
            name="Squat2", user=self.user)
        self.assertEqual(exercise.name, user_exercise.name)

    def test_admin_added_exercise_fail(self):
        """
        What if user already has an exercise with the same name?
        It does not get overwritten (success)
        """
        # GIVEN an admin user
        # WHEN they add a new exercise
        # AND user is not set

        Exercise.objects.create(
            name="Squat2",
            user=self.user,
            mechanic=self.mechanic,
            force=self.force,
            tier=self.tier,
        )

        exercise = Exercise.objects.create(
            name="Squat2",
            user=None,
            mechanic=self.mechanic,
            force=self.force,
            tier=self.tier,
        )
        # THEN the exercise should be copied out to all users
        # AND every user should have a copy of the exercise
        user_exercise = Exercise.objects.get(
            name="Squat2", user=self.user)
        self.assertEqual(exercise.name, user_exercise.name)

    def test_create_new_exercise(self):
        # GIVEN a user: user_a who has a training_focus
        # WHEN user_a creates a new exercise
        Exercise.objects.create(
            name="Squat2",
            user=self.user,
            mechanic=self.mechanic,
            force=self.force,
            tier=self.tier,
        )
        # THEN the exercise should be created
        new_exercise = Exercise.objects.get(
            name="Squat2", user=self.user
        )
        # AND a progression_type should be set
        self.assertEqual(
            new_exercise.progression_type,
            self.prog_type
        )
        # AND min_reps should be 1
        self.assertEqual(
            new_exercise.min_reps,
            1
        )
        # AND max_reps should be 5
        self.assertEqual(
            new_exercise.max_reps,
            5
        )
