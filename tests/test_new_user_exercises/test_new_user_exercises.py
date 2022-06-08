"""
GIVEN there exists a list of Exercises
WHEN a user is created
THEN the user should get assigned the Exercises in the list
"""

from django.test import TestCase

from accounts.models import User
from accounts.tests.models.factory import UserFactory
from exercises.models import Exercise

from ..factory import ExerciseFactory


class TestNewUserExercises(TestCase):
    def setUp(self):
        self.exercise = ExerciseFactory()

    def test_e2e_new_user_exercises(self):
        self.user = UserFactory()
        self.user.save()

        created_exercise = Exercise.objects.filter(
            name=self.exercise.name,
            user=self.user
        )

        self.assertTrue(created_exercise)
