from ast import For
from django.contrib import admin
from .models import Exercise, Force, Mechanic, MuscleGroup, ProgressionType, Purpose, Tier


admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Force)
admin.site.register(Tier)
admin.site.register(Purpose)
admin.site.register(Mechanic)
admin.site.register(ProgressionType)

