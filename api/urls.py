from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import ( ReadinessViewSet, readiness_answer,
    WorkoutViewSet,  WorkoutExerciseSetViewSet, 
    WorkoutExerciseViewSet, ExerciseViewSet,
    )

urlpatterns = [
    #path('readiness/', readiness),
    path('readinessanswers/', readiness_answer),
    #path('workouts/<int:pk>/', workout_detail),
    #path('workouts/<int:pk>/exercises/', workout_exercises),
    #path('workoutexercises/<int:pk>/', workoutexercise_detail),
    #path('workoutexercises/<int:pk>/sets/', workoutexercise_sets),
    #path('workoutexercisesets/<int:pk>/', workoutexerciseset_detail),
    #path('exercises/', exercises),
]

router = SimpleRouter()
router.register('readiness', ReadinessViewSet, basename='readiness')
router.register('workouts', WorkoutViewSet, basename='workouts')
router.register('workoutexercises', WorkoutExerciseViewSet, basename='workoutexercises')
router.register('workoutexercisesets', WorkoutExerciseSetViewSet, basename='workoutexercisesets')
router.register('exercises', ExerciseViewSet, basename='exercises')

urlpatterns += router.urls

