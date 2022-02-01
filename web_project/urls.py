from django.contrib import admin
from django.urls import path, include
from routines import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('routines/', include('routines.urls', namespace='routines')),
    path('exercises/', include('exercises.urls', namespace='exercises')),
]
