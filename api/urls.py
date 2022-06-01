from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (ForceViewSet, MechanicViewSet, PurposeViewSet, TierViewSet, check_token, ReadinessViewSet, readiness_answer,
                    WorkoutViewSet,  WorkoutExerciseSetViewSet,
                    WorkoutExerciseViewSet, ExerciseViewSet,
                    )

urlpatterns = [
    path('readinessanswers/', readiness_answer),
    #path('readiness/', readiness),
    #path('workouts/<int:pk>/', workout_detail),
    #path('workouts/<int:pk>/exercises/', workout_exercises),
    #path('workoutexercises/<int:pk>/', workoutexercise_detail),
    #path('workoutexercises/<int:pk>/sets/', workoutexercise_sets),
    #path('workoutexercisesets/<int:pk>/', workoutexerciseset_detail),
    #path('exercises/', exercises),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('rest-auth/check_token/', check_token),
]

router = SimpleRouter()
router.register('readiness', ReadinessViewSet, basename='readiness')
router.register('workouts', WorkoutViewSet, basename='workouts')
router.register('workoutexercises', WorkoutExerciseViewSet,
                basename='workoutexercises')
router.register('workoutexercisesets', WorkoutExerciseSetViewSet,
                basename='workoutexercisesets')
router.register('exercises', ExerciseViewSet, basename='exercises')
router.register('mechanics', MechanicViewSet, basename='mechanics')
router.register('forces', ForceViewSet, basename='forces')
router.register('purposes', PurposeViewSet, basename='purposes')
router.register('tiers', TierViewSet, basename='tiers')


urlpatterns += router.urls
