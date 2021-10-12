from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


app_name = 'accounts'

urlpatterns = [

    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/create/', views.WorkoutCreateView.as_view(), name='workout_create'),

    path('workouts/<int:pk>/', views.WorkoutItemListView.as_view(), name='workout_item_list'),
    path('workouts/<int:pk>/add/', views.WorkoutItemCreateView.as_view(), name='workout_item_add'),

    path('workouts/<int:pk>/update/', views.WorkoutUpdateView.as_view(), name='workout_update'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
