from rest_framework.routers import SimpleRouter

from .views import WorkoutExerciseSetViewSet, WorkoutExerciseViewSet

router = SimpleRouter()
router.register('workoutexercises', WorkoutExerciseViewSet, basename='workoutexercises')
router.register('workoutexercisesets', WorkoutExerciseSetViewSet, basename='workoutexercisesets')


urlpatterns = router.urls