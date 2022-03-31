from os import read
import decimal
from django.db.utils import IntegrityError
from django.test import TestCase
from exercises.models import Exercise, Progression, ProgressionType, ProgressionTypeAllocation

from routines.models import Readiness, ReadinessAnswer, ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet
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

        self.prog_type = ProgressionType.objects.create(
            name='Test',
        )

        self.prog_type_allocation = ProgressionTypeAllocation.objects.create(
            progression_type=self.prog_type,
            min_reps=1,
            max_reps=5,
            target_rir=3,
            min_rir=2
        )

        self.exercise = Exercise.objects.create(
            name="Squat",
            user=self.user_a,
            progression_type=self.prog_type
        )

        self.workout = Workout.objects.get(readiness=self.readiness)

        self.workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            is_set_adjust=True
        )

        self.progression = Progression.objects.create(
            progression_type=self.prog_type,
            rep_delta=0,
            rir_delta=-2,
            weight_change=0.05,
            rep_change=2,
            rir_change=2
        )

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
