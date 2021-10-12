from django.contrib import admin
from django.urls import path, include
from routines import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('routines/', include('routines.urls', namespace='routines')),
]
