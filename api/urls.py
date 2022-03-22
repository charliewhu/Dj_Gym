from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import exercises, readiness, workouts, workout_exercises, workoutexercise_detail, WorkoutExerciseSetViewSet, WorkoutExerciseViewSet, workoutexercise_sets, workoutexerciseset_detail

# router = SimpleRouter()
# router.register('workoutexercises', WorkoutExerciseViewSet, basename='workoutexercises')
# router.register('workoutexercisesets', WorkoutExerciseSetViewSet, basename='workoutexercisesets')
#urlpatterns = router.urls


urlpatterns = [
    path('readiness/', readiness),
    path('workouts/', workouts),
    path('workouts/<int:pk>/exercises/', workout_exercises),
    path('workoutexercises/<int:pk>/', workoutexercise_detail),
    path('workoutexercises/<int:pk>/sets/', workoutexercise_sets),
    path('workoutexercisesets/<int:pk>/', workoutexerciseset_detail),
    path('exercises/', exercises),
]