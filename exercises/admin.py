from ast import For
from django.contrib import admin
from .models import Exercise, Force, MuscleGroup


admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Force)
