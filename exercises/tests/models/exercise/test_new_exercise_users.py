"""
GIVEN there are active users
WHEN an exercise is created by the admin
AND the exercise's user is NULL
THEN the exercise should be assigned to all users
AND any existing user exercise by the same name is not overwritten
"""

from django.test import TestCase

from accounts.models import User
from accounts.tests.models.factory import UserFactory
from exercises.models import Exercise, Mechanic

from exercises.tests.models.factory import ExerciseFactory, MechanicFactory


class TestNewUserExercises(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_e2e_user_exercise_created(self):

        self.exercise = ExerciseFactory()

        created_exercise = Exercise.objects.get(
            name=self.exercise.name,
            user=self.user
        )

        self.assertTrue(created_exercise)

    def test_e2e_user_exercise_does_not_overwrite(self):
        self.exercise = ExerciseFactory(user=self.user)

        mechanic = MechanicFactory(name="test_mechanic2")

        Exercise.objects.create(
            name="test_exercise",
            mechanic=mechanic,
        )

        user_exercise = Exercise.objects.get(
            name=self.exercise.name,
            user=self.user
        )

        self.assertNotEqual(user_exercise.mechanic, mechanic)

    def test_e2e_user_exercise_isnt_assigned_to_others(self):
        # when a user creates an exercise
        # other users shouldnt be assigned it
        self.user2 = UserFactory(email="test2@test.com")

        self.exercise = ExerciseFactory(user=self.user)

        exercises = Exercise.objects.filter(
            user=self.user2
        )

        self.assertFalse(exercises)

    def test_unit_is_new_exercise(self):
        self.exercise = Exercise(name="test_exercise")
        self.assertTrue(self.exercise.is_new_exercise())

    def test_unit_has_user(self):
        pass
