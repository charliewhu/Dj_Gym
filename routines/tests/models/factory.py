from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.tests.models.factory import UserFactory
from exercises.tests.models.factory import ExerciseFactory

class ReadinessQuestionFactory(DjangoModelFactory):
    class Meta:
        model = 'readiness.ReadinessQuestion'

    name = "test_question"

class ReadinessFactory(DjangoModelFactory):
    class Meta:
        model = 'readiness.Readiness'

    user = SubFactory(UserFactory)
    date_created = "2017-01-01"

class ReadinessAnswerFactory(DjangoModelFactory):
    class Meta:
        model = 'readiness.ReadinessAnswer'

    readiness = SubFactory(ReadinessFactory)
    readiness_question = SubFactory(ReadinessQuestionFactory)
    answer = 1

class WorkoutFactory(DjangoModelFactory):
    class Meta:
        model = 'workouts.Workout'

    user = SubFactory(UserFactory)
    readiness = SubFactory(ReadinessFactory)
    date = "2017-01-01"

class WorkoutExerciseFactory(DjangoModelFactory):
    class Meta:
        model = 'workouts.WorkoutExercise'

    workout = SubFactory(WorkoutFactory)
    exercise = SubFactory(ExerciseFactory)

class WorkoutExerciseSetFactory(DjangoModelFactory):
    class Meta:
        model = 'workouts.WorkoutExerciseSet'

    workout_exercise = SubFactory(WorkoutExerciseFactory)
    weight = 100
    reps = 5
    rir = 1