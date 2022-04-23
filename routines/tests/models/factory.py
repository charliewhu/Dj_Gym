from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.tests.models.factory import UserFactory
from exercises.tests.models.factory import ExerciseFactory

class ReadinessQuestionFactory(DjangoModelFactory):
    class Meta:
        model = 'routines.ReadinessQuestion'

    name = "test_question"

class ReadinessFactory(DjangoModelFactory):
    class Meta:
        model = 'routines.Readiness'

    user = SubFactory(UserFactory)
    date_created = "2017-01-01"

class ReadinessAnswerFactory(DjangoModelFactory):
    class Meta:
        model = 'routines.ReadinessAnswer'

    readiness = SubFactory(ReadinessFactory)
    readiness_question = SubFactory(ReadinessQuestionFactory)
    answer = 1

class WorkoutFactory(DjangoModelFactory):
    class Meta:
        model = 'routines.Workout'

    user = SubFactory(UserFactory)
    date = "2017-01-01"

class WorkoutExerciseFactory(DjangoModelFactory):
    class Meta:
        model = 'routines.WorkoutExercise'

    workout = SubFactory(WorkoutFactory)
    exercise = SubFactory(ExerciseFactory)

class WorkoutExerciseSetFactory(DjangoModelFactory):
    class Meta:
        model = 'routines.WorkoutExerciseSet'

    workout_exercise = SubFactory(WorkoutExerciseFactory)
    weight = 100
    reps = 1
    rir = 0