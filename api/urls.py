from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import (
    WorkoutViewSet, exercises, readiness, workout_detail, workout_exercises, workoutexercise_detail, WorkoutExerciseSetViewSet, 
    WorkoutExerciseViewSet, workoutexercise_sets, workoutexerciseset_detail
    )

urlpatterns = [
    path('readiness/', readiness),
    #path('workouts/<int:pk>/', workout_detail),
    path('workouts/<int:pk>/exercises/', workout_exercises),
    path('workoutexercises/<int:pk>/', workoutexercise_detail),
    path('workoutexercises/<int:pk>/sets/', workoutexercise_sets),
    path('workoutexercisesets/<int:pk>/', workoutexerciseset_detail),
    path('exercises/', exercises),
]

router = SimpleRouter()
router.register('workouts', WorkoutViewSet, basename='workouts')
router.register('workoutexercises', WorkoutExerciseViewSet, basename='workoutexercises')
router.register('workoutexercisesets', WorkoutExerciseSetViewSet, basename='workoutexercisesets')

urlpatterns += router.urls

