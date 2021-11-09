from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.ExerciseListView.as_view(), name='exercise_list'),
    path('create/', views.ExerciseCreateView.as_view(), name='exercise_create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
