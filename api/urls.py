from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import readiness, WorkoutExerciseSetViewSet, WorkoutExerciseViewSet

# router = SimpleRouter()
# router.register('workoutexercises', WorkoutExerciseViewSet, basename='workoutexercises')
# router.register('workoutexercisesets', WorkoutExerciseSetViewSet, basename='workoutexercisesets')
#urlpatterns = router.urls


urlpatterns = [
    path('readiness/', readiness),

]