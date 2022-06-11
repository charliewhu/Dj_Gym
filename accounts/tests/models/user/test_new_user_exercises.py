"""
GIVEN there exists a list of Exercises
WHEN a user is created
THEN the user should get assigned the Exercises in the list
"""

from django.test import TestCase

from accounts.models import User
from accounts.tests.models.factory import UserFactory
from exercises.models import Exercise
from exercises.tests.models.factory import ExerciseFactory


class TestNewUserExercises(TestCase):
    def setUp(self):
        self.exercise = ExerciseFactory()

    def test_e2e_new_user_exercises(self):
        self.user = UserFactory()

        created_exercise = Exercise.objects.filter(
            name=self.exercise.name,
            user=self.user
        )

        self.assertTrue(created_exercise)

    def test_unit_is_new(self):
        self.user = User(email="test@test.com")
        self.assertTrue(self.user.is_new())

        self.user.id = 1
        self.assertFalse(self.user.is_new())

    def test_unit_get_exercises(self):
        self.user = User(id=1, email="test@test.com")
        self.user.save()
        self.exercise.user = self.user
        self.exercise.save()

        self.assertEquals(
            self.user.get_exercises()[0],
            Exercise.objects.all()[0]
        )
