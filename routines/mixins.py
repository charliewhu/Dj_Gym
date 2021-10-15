from django.contrib.auth.mixins import UserPassesTestMixin
from .models import MuscleGroup, Exercise, Workout, WorkoutItem

class UserWorkoutMixin(UserPassesTestMixin):
    def test_func(self):
        w = Workout.objects.get(pk=self.kwargs['pk'])
        return self.request.user.id == w.user_id


class UserWorkoutItemMixin(UserPassesTestMixin):
    def test_func(self):
        wi = WorkoutItem.objects.get(pk=self.kwargs['pk'])
        w = wi.workout
        return self.request.user.id == w.user_id