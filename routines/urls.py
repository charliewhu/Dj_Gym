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

    path('workouts/<int:pk>/', views.WorkoutItemListView.as_view(), name='workout_item_list'),
    path('workouts/<int:pk>/add', views.WorkoutItemCreateView.as_view(), name='workout_item_create'),
    path('workouts/<int:pk>/items/update/', views.WorkoutItemUpdateView.as_view(), name='workout_item_update'),
    path('workouts/<int:pk>/items/delete/', views.WorkoutItemDeleteView.as_view(), name='workout_item_delete'),

    path('ajax/load-exercises/', views.load_exercises, name='ajax_load_exercises'),

    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercises/<int:pk>/add/', views.ExerciseCreateView.as_view(), name='exercise_create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
