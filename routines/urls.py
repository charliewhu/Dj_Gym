from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.RoutineItemListView.as_view(), name='routine_list'),
    path('create/', views.RoutineItemCreateView.as_view(), name='routine_create'),
    path('<int:pk>/update/', views.RoutineItemUpdateView.as_view(), name='routine_update'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
