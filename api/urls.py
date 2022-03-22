from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import readiness, workout_exercises, workoutexercise_detail, WorkoutExerciseSetViewSet, WorkoutExerciseViewSet

# router = SimpleRouter()
# router.register('workoutexercises', WorkoutExerciseViewSet, basename='workoutexercises')
# router.register('workoutexercisesets', WorkoutExerciseSetViewSet, basename='workoutexercisesets')
#urlpatterns = router.urls


urlpatterns = [
    path('readiness/', readiness),
    path('workouts/<int:pk>/exercises/', workout_exercises),
    path('workoutexercises/<int:pk>/', workoutexercise_detail),
]