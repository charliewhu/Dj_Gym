from django.test import TestCase

from routines.models import Readiness, ReadinessAnswer, ReadinessQuestion, Workout
from accounts.models import User


class ReadinessTest(TestCase):

    def setUp(self):

        self.user_a = User.objects.create_superuser(
            email='test@test.com',
            password='some_123_password'
        )

        self.readiness_question = ReadinessQuestion.objects.create(
            name='Sleep'
        )

        self.readiness = Readiness.objects.create(user=self.user_a)

        self.workout = Workout.objects.get(readiness=self.readiness)

    def test_readiness_save(self):

        self.assertEqual(Readiness.objects.count(), 1)
        self.assertEqual(self.readiness.user.email, "test@test.com")

        # Workout should have been created as a consequence of
        # Readiness.save()
        self.assertEqual(Workout.objects.count(), 1)

    def test_readiness_percentage(self):

        ReadinessAnswer.objects.create(
            readiness=self.readiness,
            readiness_question=self.readiness_question,
            rating=1
        )

        self.assertEqual(self.readiness.percentage(), 20)

    def test_readiness_get_workout(self):
        self.assertEqual(self.readiness.get_workout(), self.workout)
