from django.contrib.auth.mixins import UserPassesTestMixin
from .models import MuscleGroup, Exercise, Workout, WorkoutExercise, WorkoutExerciseSet


class UserWorkoutMixin(UserPassesTestMixin):
    def test_func(self):
        w = Workout.objects.get(pk=self.kwargs['pk'])
        return self.request.user.id == w.user_id


class UserWorkoutExerciseMixin(UserPassesTestMixin):
    def test_func(self):
        we = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        w = we.workout
        return self.request.user.id == w.user_id


class UserWorkoutExerciseSetMixin(UserPassesTestMixin):
    def test_func(self):
        wes = WorkoutExerciseSet.objects.get(pk=self.kwargs['pk'])
        we = WorkoutExercise.objects.get(id=wes.workout_exercise.id)
        w = we.workout
        return self.request.user.id == w.user_id