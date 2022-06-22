from decimal import Decimal
import json
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.tests.models.factory import TrainingFocusFactory, UserFactory
from api.views import generate_next_set
from exercises.tests.models.factory import ExerciseFactory, ProgressionFactory, ProgressionTypeAllocationFactory
from routines.models import WorkoutExerciseSet
from routines.tests.models.factory import WorkoutExerciseFactory, WorkoutFactory


class TestWorkoutExerciseSetGenerate(TestCase):
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

        client = APIClient()
        client.force_authenticate(user=self.user)

    def test_e2e_api_set_generate(self):
        """
        GIVEN an authenticated user
        AND they have a WorkoutExerciseSet with pk
        WHEN they POST to /api/workout_exercise_sets/<pk>/next_set
        THEN a response is returned with the next WorkoutExerciseSet of the WorkoutExercise
        """

        self.workout_exercise_set = WorkoutExerciseSet.objects.create(
            workout_exercise=self.workout_exercise,
            weight=100,
            reps=8,
            rir=0
        )

        view = generate_next_set
        pk = self.workout_exercise_set.id
        url = f'/api/workoutexercisesets/{pk}/generate_next_set/'

        response = self.client.post(url)

        self.assertEqual(
            response.data,
            {
                'id': 1,
                'workout_exercise': 1,
                'weight': Decimal('100.0'),
                'reps': 8,
                'rir': 0
            }
        )
