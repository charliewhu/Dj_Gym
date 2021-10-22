from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


app_name = 'routines'

urlpatterns = [

    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/create/', views.WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/<int:pk>/update/', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout_delete'),

    path('workouts/<int:pk>/', views.WorkoutExerciseListView.as_view(), name='workout_exercise_list'),
    path('workouts/<int:pk>/add', views.WorkoutExerciseCreateView.as_view(), name='workout_exercise_create'),
    path('workouts/exercise/<int:pk>/update/', views.WorkoutExerciseUpdateView.as_view(), name='workout_exercise_update'),
    path('workouts/exercise/<int:pk>/delete/', views.WorkoutExerciseDeleteView.as_view(), name='workout_exercise_delete'),
    path('ajax/load-exercises/', views.load_exercises, name='ajax_load_exercises'),

    path('workouts/exercise/<int:pk>/', views.WorkoutExerciseSetListView.as_view(), name='wo_ex_set_list'),
    path('workouts/exercise/<int:pk>/add', views.WorkoutExerciseSetCreateView.as_view(), name='wo_ex_set_create'),
    path('workouts/exercise/set/<int:pk>/update', views.WorkoutExerciseSetUpdateView.as_view(), name='wo_ex_set_update'),
    path('workouts/exercise/set/<int:pk>/delete', views.WorkoutExerciseSetDeleteView.as_view(), name='wo_ex_set_delete'),


    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercises/<int:pk>/add/', views.ExerciseCreateView.as_view(), name='exercise_create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
